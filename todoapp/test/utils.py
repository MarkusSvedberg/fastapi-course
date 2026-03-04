from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import pytest

from todoapp.models import Todos, Users
from todoapp.database import Base, get_db
from todoapp.main import app
from todoapp.routers.auth import get_current_user, bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./todoapp/testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user_admin():
    return {"username": "markus", "id": 1, "user_role": "admin"}

def override_get_current_user():
    return {"username": "markus", "id": 1, "user_role": "user"}

@pytest.fixture()
def admin_overrides():
    # Apply overrides
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user_admin

    yield # Let the test run

    # Clean up overrides after the test completes
    app.dependency_overrides = {}

@pytest.fixture()
def user_overrides():
    # Apply overrides
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    yield # Let the test run

    # Clean up overrides after the test completes
    app.dependency_overrides = {}

@pytest.fixture()
def db_override():
    # Apply overrides
    app.dependency_overrides[get_db] = override_get_db

    yield # Let the test run

    # Clean up overrides after the test completes
    app.dependency_overrides = {}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code!",
        description = "Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username = "markus",
        email = "test@test.com",
        first_name="markus",
        last_name="svedberg",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="076 123 24 69"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

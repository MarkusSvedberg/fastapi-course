from starlette import status
from todoapp.test.utils import *

def test_admin_read_all_authenticated(test_todo, admin_overrides):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{ "title": "Learn to code!", "description": "Need to learn everyday!", "priority":5, "complete":False, "owner_id": 1, "id": 1 }]

def test_admin_read_all_unauthenticated(test_todo, user_overrides):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not admin user"}

def test_admin_delete_todo(test_todo, admin_overrides):
    response = client.delete("/admin/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_admin_delete_todo_unauthorized(test_todo, user_overrides):
    response = client.delete("/admin/todos/1")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { "title": "Learn to code!", "description": "Need to learn everyday!", "priority":5, "complete":False, "owner_id": 1, "id": 1 }

def test_admin_delete_todo_not_found(test_todo, admin_overrides):
    response = client.delete("/admin/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_admin_delete_todo_not_found_unauthorized(test_todo, user_overrides):
    response = client.delete("/admin/todos/999")
    assert response.status_code == status.HTTP_403_FORBIDDEN

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from todoapp.models import Users
from todoapp.database import SessionLocal
from todoapp.routers.auth import get_current_user, bcrypt_context

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6)
    verify_password: str = Field(min_length=6)

@router.get("/get_user", status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Not authorized")

    user_data = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")

    return user_data

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, change_password_request: ChangePasswordRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Not authorized")

    user_data = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")

    if not bcrypt_context.verify(change_password_request.old_password, user_data.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Incorrect old password")

    if change_password_request.new_password != change_password_request.verify_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail = "New passwords do not match")

    user_data.hashed_password = bcrypt_context.hash(change_password_request.new_password)

    db.add(user_data)
    db.commit()

@router.put("/change_phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Not authorized")

    user_data = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")

    user_data.phone_number = phone_number

    db.add(user_data)
    db.commit()

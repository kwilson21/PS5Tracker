from datetime import timedelta
from typing import Dict
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

from app.db import models
from app.db import schemas
from app.db import user_store
from app.db.user_store import verify_password
from app.dependencies import manager

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:  # noqa: B008
    email = data.username
    password = data.password

    user = user_store.get_user_by_email(email)
    if not user:
        raise InvalidCredentialsException
    elif not verify_password(password, user.password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": email}, expires=timedelta(hours=12))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate) -> schemas.User:
    db_user = user_store.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_store.create_user(user=user)


@router.get("/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100) -> List[schemas.User]:
    users = user_store.get_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int) -> models.User:
    db_user = user_store.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

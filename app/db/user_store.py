from passlib.context import CryptContext

from app.db import models
from app.db import schemas
from app.dependencies import manager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(user_id: int):
    return models.User.get_by_id(user_id)


@manager.user_loader
def get_user_by_email(email: str):
    return models.User.get(models.User.email == email)


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    db_user.save()
    return db_user

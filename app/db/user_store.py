import re

from passlib.context import CryptContext

from app.db import models
from app.db import schemas
from app.dependencies import manager
from app.exceptions import ValidationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_regex = re.compile("^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])")  # noqa: W605


def validate_password(password: str) -> bool:
    valid = password_regex.match(password)

    if not valid:
        raise ValidationError(
            (
                "Invalid password. Password must meet the following conditions: "
                "6-20 characters long, "
                "Include at least 1 digit, "
                "At least 1 uppercase and lowercase letter, "
                "At least 1 special character"
            )
        )
    return bool(valid)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


@manager.user_loader
def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    validate_password(user.password)
    hashed_password = get_password_hash(user.password)
    db_user = models.User.create(email=user.email, password=hashed_password)
    db_user.save()
    return db_user

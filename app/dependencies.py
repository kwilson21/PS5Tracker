from fastapi import Depends
from fastapi_login import LoginManager

from app import settings
from app.db.models import db_state_default
from app.db.models import mysql_db
from app.exceptions import NotAuthenticatedException


async def reset_db_state():
    mysql_db._state._state.set(db_state_default.copy())
    mysql_db._state.reset()


def get_db(db_state=Depends(reset_db_state)):  # noqa: B008
    try:
        mysql_db.connect()
        yield
    finally:
        if not mysql_db.is_closed():
            mysql_db.close()


manager = LoginManager(settings.SECRET_KEY, token_url="/auth/token")
manager.not_authenticated_exception = NotAuthenticatedException

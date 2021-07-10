from fastapi_login import LoginManager

from app import settings
from app.exceptions import NotAuthenticatedException


manager = LoginManager(settings.SECRET_KEY, token_url="/auth/token")
manager.not_authenticated_exception = NotAuthenticatedException

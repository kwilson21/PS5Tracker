from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DB_NAME = config("DATABASE_NAME")
DB_USER = config("DATABASE_USER")
DB_PASS = config("DATABASE_PASSWORD")
DB_HOST = config("DATABASE_HOST", default="localhost")
DB_PORT = config("DATABASE_PORT", cast=int, default=3306)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="127.0.0.1,localhost")
APP_ENV = config("APP_ENV", default="development")

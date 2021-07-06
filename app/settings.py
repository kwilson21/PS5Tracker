from shutil import which

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings


config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DB_NAME = config("DATABASE_NAME", default="PS5Tracker")
DB_USER = config("DATABASE_USER", default="root")
DB_PASS = config("DATABASE_PASSWORD", cast=str, default="1234")
DB_HOST = config("DATABASE_HOST", default="localhost")
DB_PORT = config("DATABASE_PORT", cast=int, default=3306)
DB_URL = config("JAWSDB_MARIA_URL", default=None)
HOST = config("HOST", default="localhost")
PORT = config("PORT", cast=int, default=8000)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="127.0.0.1,localhost")
APP_ENV = config("APP_ENV", default="development")
CHROME_DRIVER_EXECUTABLE_PATH = config("CHROME_DRIVER_EXECUTABLE_PATH", default=which("chromedriver"))
CHROME_BINARY_LOCATION = which("google-chrome") or "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_URL = config("REDISTOGO_URL", default=None)
URL = config("URL", default="localhost")
TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", default=None)
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", default=None)
TEST_EMAIL = config("TEST_EMAIL", default=None)
TEST_PHONE_NUMBER = config("TEST_PHONE_NUMBER", default=None)

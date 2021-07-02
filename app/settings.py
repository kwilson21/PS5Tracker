from shutil import which

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DB_NAME = config("DATABASE_NAME")
DB_USER = config("DATABASE_USER")
DB_PASS = config("DATABASE_PASSWORD")
DB_HOST = config("DATABASE_HOST", default="localhost")
DB_PORT = config("DATABASE_PORT", cast=int, default=3306)
HOST = config("HOST", default="localhost")
PORT = config("PORT", cast=int, default=8000)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="127.0.0.1,localhost")
APP_ENV = config("APP_ENV", default="development")
SELENIUM_DRIVER_EXECUTABLE_PATH = config("SELENIUM_DRIVER_EXECUTABLE_PATH", default=which("chromedriver"))
SELENIUM_DRIVER_ARGUMENTS = ["--headless", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1920,1080", "--disable-extensions", "--proxy-server='direct://'", "--proxy-bypass-list=*", "--start-maximized", "--disable-gpu", "--ignore-certificate-errors", "--test-type", "--no-first-run", "--no-default-browser-check"]
CHROME_BINARY_LOCATION = which("google-chrome") or "C:\Program Files\Google\Chrome\Application\chrome.exe"
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_URL = config("REDIS_URL", default=None)

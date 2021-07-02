from contextlib import contextmanager

from selenium import webdriver

from app import settings


@contextmanager
def driver_ctx():
    options = webdriver.ChromeOptions()
    options.binary_location = settings.CHROME_BINARY_LOCATION
    options.add_argument(settings.SELENIUM_DRIVER_ARGUMENTS)
    driver = webdriver.Chrome(settings.SELENIUM_DRIVER_EXECUTABLE_PATH, chrome_options=options)

    yield driver

    driver.close()

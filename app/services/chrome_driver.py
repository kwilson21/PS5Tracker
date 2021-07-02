from contextlib import contextmanager

from selenium import webdriver

from app import settings


@contextmanager
def driver_ctx():
    options = webdriver.ChromeOptions()
    options.binary_location = settings.CHROME_BINARY_LOCATION
    for arg in settings.SELENIUM_DRIVER_ARGUMENTS:
        options.add_argument(arg)
    driver = webdriver.Chrome(settings.SELENIUM_DRIVER_EXECUTABLE_PATH, chrome_options=options)

    driver.implicitly_wait(3)

    try:
        yield driver
    finally:
        driver.quit()

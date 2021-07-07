from contextlib import contextmanager

from selenium import webdriver

from app import settings


@contextmanager
def driver_ctx():
    options = webdriver.ChromeOptions()
    options.binary_location = settings.CHROME_BINARY_LOCATION
    options.headless = True

    driver = webdriver.Chrome(settings.CHROME_DRIVER_EXECUTABLE_PATH, chrome_options=options)

    # options = webdriver.FirefoxOptions()
    # options.headless = True
    # driver = webdriver.Firefox(options=options, service_log_path='/dev/null')

    try:
        yield driver
    finally:
        driver.quit()

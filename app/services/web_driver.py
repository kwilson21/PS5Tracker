from contextlib import contextmanager

from selenium import webdriver

from app import settings


def _get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = settings.CHROME_BINARY_LOCATION
    options.headless = True
    return webdriver.Chrome(settings.CHROME_DRIVER_EXECUTABLE_PATH, chrome_options=options)


def _get_firefox_driver():
    options = webdriver.FirefoxOptions()
    options.headless = True
    return webdriver.Firefox(options=options, service_log_path="/dev/null")


@contextmanager
def driver_ctx(use_driver: str = settings.WEB_DRIVER):
    if use_driver == "chrome":
        driver = _get_chrome_driver()
    elif use_driver == "firefox":
        driver = _get_firefox_driver()
    else:
        raise Exception("Invalid driver specified")

    try:
        yield driver
    finally:
        driver.quit()

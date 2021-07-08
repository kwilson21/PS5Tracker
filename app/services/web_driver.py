import os
from contextlib import contextmanager

import undetected_chromedriver.v2 as uc
from selenium import webdriver

from app import settings


def _get_chrome_driver():
    options = uc.ChromeOptions()
    options.binary_location = settings.CHROME_BINARY_LOCATION
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("user-data-dir=selenium")
    return uc.Chrome(options=options, service_log_path=os.path.devnull)


def _get_firefox_driver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference("useAutomationExtension", False)
    profile.update_preferences()
    desired = webdriver.DesiredCapabilities.FIREFOX
    options = webdriver.FirefoxOptions()
    options.headless = True
    return webdriver.Firefox(
        options=options, service_log_path=os.path.devnull, firefox_profile=profile, desired_capabilities=desired
    )


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

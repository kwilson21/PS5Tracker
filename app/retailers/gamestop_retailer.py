from datetime import datetime
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.constants import GAMESTOP_RETAILER
from app.db.models import RetailerInfo
from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.retailer import Retailer as RetailerModel
from app.models.stock_status import StockStatus
from app.retailers.retailer import Retailer
from app.services.web_driver import driver_ctx


class GameStopRetailer(Retailer):
    DISC_VERSION_URL = (
        "https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html"
    )
    DIGITAL_VERSION_URL = (
        "https://www.gamestop.com/video-games/playstation-5/consoles/products/"
        "playstation-5-digital-edition/11108141.html"
    )

    @property
    def offered_versions(self) -> List[PS5Version]:
        return [PS5Version.DISC, PS5Version.DIGITAL]

    def get_availability(self, ps5_version: PS5Version) -> Availability:
        with driver_ctx() as driver:
            if ps5_version is PS5Version.DISC:
                driver.get(self.DISC_VERSION_URL)
            elif ps5_version is PS5Version.DIGITAL:
                driver.get(self.DIGITAL_VERSION_URL)
            else:
                raise ValueError(f"Incorrect ps5 version {ps5_version}")

            price_xpath = '//*[@id="primary-details-row"]/div[2]/div/div/span/span[2]/span'
            stock_xpath = '//*[@id="add-to-cart"]'

            price_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, price_xpath)))

            price = price_element.text.replace("$", "")

            stock_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, stock_xpath)))

            if "NOT AVAILABLE" in stock_element.text:
                stock_status = StockStatus.OUT_OF_STOCK
            elif "Add to Cart" in stock_element.text:
                stock_status = StockStatus.IN_STOCK
            else:
                raise Exception(f"Unknown stock status {stock_element.text=}")

        return Availability(version=ps5_version, stock_status=stock_status, price=price, updated_at=datetime.now())

    def get_availabilities(self) -> List[Availability]:
        return [self.get_availability(ps5_version) for ps5_version in self.offered_versions]

    def get_retailer_availabilities(self) -> RetailerModel:
        retailer = RetailerModel(name=GAMESTOP_RETAILER, availabilities=self.get_availabilities())

        return retailer

    def attempt_purchase(self, retailer_info: RetailerInfo, price: str) -> bool:
        raise NotImplementedError()

from datetime import datetime
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.constants import NEW_EGG_RETAILER
from app.constants import PS5_DIGITAL_MSRP
from app.constants import PS5_DISC_MSRP
from app.db.models import RetailerInfo
from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.retailer import Retailer as RetailerModel
from app.models.stock_status import StockStatus
from app.retailers.retailer import Retailer
from app.services.web_driver import driver_ctx


class NeweggRetailer(Retailer):
    DIGITAL_VERSION_URL = "https://www.newegg.com/p/N82E16868110289?Description=ps5&cm_re=ps5-_-68-110-289-_-Product"

    @property
    def offered_versions(self) -> List[PS5Version]:
        return [PS5Version.DIGITAL]

    def get_availability(self, ps5_version: PS5Version) -> Availability:
        with driver_ctx() as driver:
            if ps5_version is PS5Version.DIGITAL:
                driver.get(self.DIGITAL_VERSION_URL)
            else:
                raise ValueError(f"Incorrect ps5 version {ps5_version}")

            price_xpath = '//*[@id="app"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/ul/li[3]/strong'
            stock_xpath = '//*[@id="app"]/div[2]/div[1]/div/div/div[2]/div[1]/div[5]/div[3]/div[1]/strong'

            price_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, price_xpath)))

            price = price_element.text.replace("$", "")

            if price in PS5_DISC_MSRP:
                price = PS5_DISC_MSRP
            elif price in PS5_DIGITAL_MSRP:
                price = PS5_DIGITAL_MSRP

            stock_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, stock_xpath)))

            stock_status = StockStatus.IN_STOCK if "In stock." in stock_element.text else StockStatus.OUT_OF_STOCK

        return Availability(version=ps5_version, stock_status=stock_status, price=price, updated_at=datetime.now())

    def get_availabilities(self) -> List[Availability]:
        return [self.get_availability(ps5_version) for ps5_version in self.offered_versions]

    def get_retailer_availabilities(self) -> RetailerModel:
        retailer = RetailerModel(name=NEW_EGG_RETAILER, availabilities=self.get_availabilities())

        return retailer

    def attempt_purchase(self, retailer_info: RetailerInfo, price: str) -> bool:
        raise NotImplementedError()

from datetime import datetime
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.constants import TARGET_RETAILER
from app.db.models import RetailerInfo
from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.retailer import Retailer as RetailerModel
from app.models.stock_status import StockStatus
from app.retailers.retailer import Retailer
from app.services.web_driver import driver_ctx


class TargetRetailer(Retailer):
    DISC_VERSION_URL = "https://www.target.com/p/playstation-5-console/-/A-81114595#lnk=sametab"
    DIGITAL_VERSION_URL = "https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596#lnk=sametab"

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

            price_xpath = '//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div'
            stock_xpath = '//*[@id="viewport"]/div[4]/div/div[2]/div[3]/div[1]/div/div/div'

            price_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, price_xpath)))

            price = price_element.text.replace("$", "")

            stock_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, stock_xpath)))

            out_of_stock_texts = ["Sold out", "Out of stock"]

            out_of_stock = any(out_of_stock_text in stock_element.text for out_of_stock_text in out_of_stock_texts)

            stock_status = StockStatus.OUT_OF_STOCK if out_of_stock else StockStatus.IN_STOCK

        return Availability(version=ps5_version, stock_status=stock_status, price=price, updated_at=datetime.now())

    def get_availabilities(self) -> List[Availability]:
        return [self.get_availability(ps5_version) for ps5_version in self.offered_versions]

    def get_retailer_availabilities(self) -> RetailerModel:
        retailer = RetailerModel(name=TARGET_RETAILER, availabilities=self.get_availabilities())

        return retailer

    def attempt_purchase(self, retailer_info: RetailerInfo, price: str) -> bool:
        raise NotImplementedError()

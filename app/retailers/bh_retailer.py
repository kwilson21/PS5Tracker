from datetime import datetime
from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.constants import BH_RETAILER
from app.db.models import RetailerInfo
from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.retailer import Retailer as RetailerModel
from app.models.stock_status import StockStatus
from app.retailers.retailer import Retailer
from app.services.web_driver import driver_ctx


class BHRetailer(Retailer):
    DISC_VERSION_URL = (
        "https://www.bhphotovideo.com/c/product/1595083-REG/sony_3005718_playstation_5_gaming_console.html"
    )

    @property
    def offered_versions(self) -> List[PS5Version]:
        return [PS5Version.DISC]

    def get_availability(self, ps5_version: PS5Version) -> Availability:
        with driver_ctx() as driver:
            if ps5_version is PS5Version.DISC:
                driver.get(self.DISC_VERSION_URL)
            else:
                raise ValueError(f"Incorrect ps5 version {ps5_version}")

            price_xpath = (
                "//*[@id='bh-app']/section/div/div[2]/div[5]/div/div[2]/div/div/div[2]/div/div/div"
                "[contains(@data-selenium,'pricingPrice')]"
            )
            in_stock_xpath = (
                '//*[@id="bh-app"]/section/div/div[2]/div[5]/div/div[2]/div/div/div[4]/div[1]/div[1]/button[1]'
            )
            out_of_stock_xpath = (
                '//*[@id="bh-app"]/section/div/div[2]/div[5]/div/div[2]/div/div/div[5]/div[1]/div[1]/div/button'
            )

            price_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, price_xpath)))

            price = price_element.text.replace("$", "")

            try:
                stock_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, in_stock_xpath))
                )
            except TimeoutException:
                stock_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, out_of_stock_xpath))
                )

            if "Notify When Available" in stock_element.text:
                stock_status = StockStatus.OUT_OF_STOCK
            elif "Add to Cart" in stock_element.text:
                stock_status = StockStatus.IN_STOCK
            else:
                raise Exception(f"Unknown stock status {stock_element.text=}")

        return Availability(version=ps5_version, stock_status=stock_status, price=price, updated_at=datetime.now())

    def get_availabilities(self) -> List[Availability]:
        return [self.get_availability(ps5_version) for ps5_version in self.offered_versions]

    def get_retailer_availabilities(self) -> RetailerModel:
        retailer = RetailerModel(name=BH_RETAILER, availabilities=self.get_availabilities())

        return retailer

    def attempt_purchase(self, retailer_info: RetailerInfo, price: str) -> bool:
        raise NotImplementedError()

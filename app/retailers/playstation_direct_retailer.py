from datetime import datetime
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.constants import PLAYSTATION_DIRECT_RETAILER
from app.constants import PS5_DIGITAL_MSRP
from app.constants import PS5_DISC_MSRP
from app.db.models import RetailerInfo
from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.retailer import Retailer as RetailerModel
from app.models.stock_status import StockStatus
from app.retailers.retailer import Retailer
from app.services.web_driver import driver_ctx


class PlaystationDirectRetailer(Retailer):
    DISC_VERSION_URL = "https://direct.playstation.com/en-us/consoles/console/playstation5-console.3005816"
    DIGITAL_VERSION_URL = (
        "https://direct.playstation.com/en-us/consoles/console/playstation5-digital-edition-console.3005817"
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

            price_xpath = (
                "/html/body/div[1]/div/div[3]/producthero-component"
                "/div/div/div[3]/producthero-info/div/div[1]/div[1]/span"
            )
            in_stock_xpath = (
                "/html/body/div[1]/div/div[3]/producthero-component/div/div/div[3]/producthero-info/div/div[4]/button"
            )
            out_of_stock_xpath = (
                "/html/body/div[1]/div/div[3]/producthero-component/div/div/div[3]/producthero-info/div/div[4]/div[2]/p"
            )

            price_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, price_xpath)))

            price = price_element.text.replace("$", "")

            if price in PS5_DISC_MSRP:
                price = PS5_DISC_MSRP
            elif price in PS5_DIGITAL_MSRP:
                price = PS5_DIGITAL_MSRP

            stock_element = None
            try:
                stock_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, in_stock_xpath))
                )
            except NoSuchElementException:
                pass

            if not stock_element:
                stock_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, out_of_stock_xpath))
                )

            if "Out of Stock" in stock_element.text:
                stock_status = StockStatus.OUT_OF_STOCK
            elif "Add" in stock_element.text:
                stock_status = StockStatus.IN_STOCK
            else:
                raise Exception(f"Unknown stock status {stock_element.text=}")

        return Availability(version=ps5_version, stock_status=stock_status, price=price, updated_at=datetime.now())

    def get_availabilities(self) -> List[Availability]:
        return [self.get_availability(ps5_version) for ps5_version in self.offered_versions]

    def get_retailer_availabilities(self) -> RetailerModel:
        retailer = RetailerModel(name=PLAYSTATION_DIRECT_RETAILER, availabilities=self.get_availabilities())

        return retailer

    def attempt_purchase(self, retailer_info: RetailerInfo, price: str) -> bool:
        raise NotImplementedError()

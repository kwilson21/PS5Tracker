from datetime import datetime
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.constants import BEST_BUY_RETAILER
from app.constants import PS5_VERSIONS
from app.db.models import RetailerInfo
from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.retailer import Retailer as RetailerModel
from app.models.stock_status import StockStatus
from app.retailers.retailer import Retailer
from app.services.chrome_driver import driver_ctx


class BestBuyRetailer(Retailer):
    DISC_VERSION_URL = "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149"
    DIGITAL_VERSION_URL = (
        "https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161"
    )

    def get_availability(self, ps5_version: PS5Version) -> Availability:
        with driver_ctx() as driver:
            if ps5_version is PS5Version.DISC:
                driver.get(self.DISC_VERSION_URL)
            elif ps5_version is PS5Version.DIGITAL:
                driver.get(self.DIGITAL_VERSION_URL)
            else:
                raise ValueError(f"Incorrect ps5 version {ps5_version}")

            price_xpath = '//*[@id="pricing-price-91991087"]/div/div/div/div/div[2]/div[1]/div/div/span[1]'
            stock_xpath = '//*[@id="fulfillment-add-to-cart-button-966791"]/div/div/div/button'

            price_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, price_xpath)))

            price = price_element.text.replace("$", "")

            stock_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, stock_xpath)))

            if stock_element.text == "Sold Out":
                stock_status = StockStatus.OUT_OF_STOCK
            elif stock_element.text == "Add to Cart":
                stock_status = StockStatus.IN_STOCK
            else:
                raise Exception(f"Unknown stock status {stock_element.text=}")

        return Availability(version=ps5_version, stock_status=stock_status, price=price, updated_at=datetime.now())

    def get_availabilities(self) -> List[Availability]:
        return [self.get_availability(ps5_version) for ps5_version in PS5_VERSIONS]

    def get_retailer_availabilities(self) -> RetailerModel:
        retailer = RetailerModel(name=BEST_BUY_RETAILER, availabilities=self.get_availabilities())

        return retailer

    def attempt_purchase(self, retailer_info: RetailerInfo, price: str) -> bool:
        raise NotImplementedError()

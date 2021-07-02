from app.db.models import RetailerInfo
from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.stock_status import StockStatus
from app.retailers.retailer import Retailer
from app.services.chrome_driver import driver_ctx


class TargetRetailer(Retailer):
    DISC_VERSION_URL = "https://www.target.com/p/playstation-5-console/-/A-81114595#lnk=sametab"
    DIGITAL_VERSION_URL = "https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596#lnk=sametab"

    def get_availability(self, ps5_version: PS5Version) -> Availability:
        with driver_ctx() as driver:
            if ps5_version == PS5Version.DISC:
                driver.get(self.DISC_VERSION_URL)
            elif ps5_version == PS5Version.DIGITAL:
                driver.get(self.DIGITAL_VERSION_URL)

            price_element = driver.find_element_by_xpath(
                '//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div'
            )
            price = price_element.text

            stock_element = driver.find_element_by_xpath(
                '//*[@id="viewport"]/div[4]/div/div[2]/div[3]/div[1]/div/div/div'
            )

            stock_status = StockStatus.OUT_OF_STOCK if stock_element.text == "Sold out" else StockStatus.IN_STOCK

        return Availability(version=ps5_version, stock_status=stock_status, price=price)

    def attempt_purchase(self, retailer_info: RetailerInfo, price: str) -> bool:
        raise NotImplementedError()

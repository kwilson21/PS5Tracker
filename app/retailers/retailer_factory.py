from app.constants import TARGET_RETAILER
from app.retailers.retailer import Retailer
from app.retailers.target_retailer import TargetRetailer


class RetailerFactory:
    @staticmethod
    def get_retailer(retailer_name: str) -> Retailer:
        if retailer_name == TARGET_RETAILER:
            return TargetRetailer()
        raise Exception(f"Invalid retailer name {retailer_name}")

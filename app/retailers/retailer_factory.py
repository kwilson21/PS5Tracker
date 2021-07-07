from app.constants import BEST_BUY_RETAILER
from app.constants import TARGET_RETAILER
from app.retailers.best_buy_retailer import BestBuyRetailer
from app.retailers.retailer import Retailer
from app.retailers.target_retailer import TargetRetailer


class RetailerFactory:
    @staticmethod
    def get_retailer(retailer_name: str) -> Retailer:
        if retailer_name == TARGET_RETAILER:
            return TargetRetailer()
        if retailer_name == BEST_BUY_RETAILER:
            return BestBuyRetailer()
        raise ValueError(f"Invalid retailer name {retailer_name}")

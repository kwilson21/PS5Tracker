from app.constants import ADORAMA_RETAILER
from app.constants import BEST_BUY_RETAILER
from app.constants import BH_RETAILER
from app.constants import GAMESTOP_RETAILER
from app.constants import NEW_EGG_RETAILER
from app.constants import PLAYSTATION_DIRECT_RETAILER
from app.constants import TARGET_RETAILER
from app.retailers.adorama_retailer import AdoramaRetailer
from app.retailers.best_buy_retailer import BestBuyRetailer
from app.retailers.bh_retailer import BHRetailer
from app.retailers.gamestop_retailer import GameStopRetailer
from app.retailers.new_egg_retailer import NeweggRetailer
from app.retailers.playstation_direct_retailer import PlaystationDirectRetailer
from app.retailers.retailer import Retailer
from app.retailers.target_retailer import TargetRetailer


class RetailerFactory:
    @staticmethod
    def get_retailer(retailer_name: str) -> Retailer:
        if retailer_name == TARGET_RETAILER:
            return TargetRetailer()
        elif retailer_name == BEST_BUY_RETAILER:
            return BestBuyRetailer()
        elif retailer_name == NEW_EGG_RETAILER:
            return NeweggRetailer()
        elif retailer_name == ADORAMA_RETAILER:
            return AdoramaRetailer()
        elif retailer_name == PLAYSTATION_DIRECT_RETAILER:
            return PlaystationDirectRetailer()
        elif retailer_name == GAMESTOP_RETAILER:
            return GameStopRetailer()
        elif retailer_name == BH_RETAILER:
            return BHRetailer()
        raise ValueError(f"Invalid retailer name {retailer_name}")

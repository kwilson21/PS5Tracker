from typing import List
from typing import Optional

from app.constants import RETAILER_REDIS_CONN
from app.constants import RETAILERS
from app.models.retailer import Retailer as RetailerModel


def update_retailer_availabilities(retailer: RetailerModel) -> bool:
    return RETAILER_REDIS_CONN.set(retailer.name, retailer.json())  # type: ignore


def get_all_retailer_availabilities() -> List[RetailerModel]:
    retailer_availabilities: List[RetailerModel] = []
    for retailer_name in RETAILERS:
        retailer_str = RETAILER_REDIS_CONN.get(retailer_name)
        if retailer_str:
            retailer_availabilities.append(RetailerModel.parse_raw(retailer_str))
    return retailer_availabilities


def get_retailer_availability(retailer_name: str) -> Optional[RetailerModel]:
    retailer_str = RETAILER_REDIS_CONN.get(retailer_name)
    if retailer_str:
        return RetailerModel.parse_raw(retailer_str)
    return None


def delete_retailer_availability(retailer_name: str) -> bool:
    return bool(RETAILER_REDIS_CONN.delete(retailer_name))


def delete_all_retailer_availabilities() -> bool:
    for retailer_name in RETAILERS:
        delete_retailer_availability(retailer_name)
    return True

import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from app.constants import RETAILER_REDIS_CONN
from app.constants import RETAILERS
from app.models.retailer import Retailer


def update_retailer_availabilities(retailer: Retailer) -> bool:
    return RETAILER_REDIS_CONN.set(retailer.name, retailer.to_json())  # type: ignore


def get_all_retailer_availabilities() -> List[Dict[str, Any]]:
    retailer_availabilities: List[Dict[str, Any]] = []
    for retailer_name in RETAILERS:
        retailer_str = RETAILER_REDIS_CONN.get(retailer_name)
        if retailer_str:
            retailer_availabilities.append(json.loads(retailer_str))
    return retailer_availabilities


def get_retailer_availabilitiy(retailer_name: str) -> Optional[Retailer]:
    retailer_str = RETAILER_REDIS_CONN.get(retailer_name)
    if retailer_str:
        return Retailer.from_json(retailer_str)  # type: ignore
    return None


def delete_retailer_availabilitiy(retailer_name: str) -> bool:
    return bool(RETAILER_REDIS_CONN.delete(retailer_name))


def delete_all_retailer_availabilities() -> bool:
    for retailer_name in RETAILERS:
        delete_retailer_availabilitiy(retailer_name)
    return True

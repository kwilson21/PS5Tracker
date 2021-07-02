import json
from typing import Any
from typing import Dict

import redis

from app import settings
from app.constants import RETAILERS
from app.models.retailer import Retailer

retailer_availability_db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def update_retailer_availabilities(retailer: Retailer) -> bool:
    return retailer_availability_db.set(retailer.name, retailer.to_json())


def get_all_retailer_availabilities() -> Dict[str, Any]:
    return [json.loads(retailer_availability_db.get(retailer_name)) for retailer_name in RETAILERS]


def get_retailer_availabilitiy(retailer_name: str) -> Retailer:
    return Retailer.from_json(retailer_availability_db.get(retailer_name))


def delete_retailer_availabilitiy(retailer_name: str) -> bool:
    return retailer_availability_db.delete(retailer_name)


def delete_all_retailer_availabilities() -> bool:
    for retailer_name in RETAILERS:
        delete_retailer_availabilitiy(retailer_name)
    return True

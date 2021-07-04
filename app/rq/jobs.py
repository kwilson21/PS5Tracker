from app.constants import RETAILER_AVAILABILITY_REDIS_CHANNEL
from app.constants import RETAILER_REDIS_CONN
from app.constants import TARGET_RETAILER
from app.db import retailer_store
from app.retailers.retailer_factory import RetailerFactory


def update_target_retailer_availabilities() -> None:
    target_retailer = RetailerFactory.get_retailer(TARGET_RETAILER)

    retailer_availabilities = target_retailer.get_retailer_availabilities()

    retailer_store.update_retailer_availabilities(retailer_availabilities)

    RETAILER_REDIS_CONN.publish(RETAILER_AVAILABILITY_REDIS_CHANNEL, retailer_availabilities.to_json())  # type: ignore


all_jobs = [update_target_retailer_availabilities]

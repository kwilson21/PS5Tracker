from app.constants import RETAILER_AVAILABILITY_REDIS_CHANNEL
from app.constants import RETAILER_REDIS_CONN
from app.db import retailer_store
from app.retailers.retailer_factory import RetailerFactory


def update_retailer_availabilities(retailer_name: str) -> None:
    retailer = RetailerFactory.get_retailer(retailer_name)

    retailer_availabilities = retailer.get_retailer_availabilities()

    retailer_store.update_retailer_availabilities(retailer_availabilities)

    RETAILER_REDIS_CONN.publish(RETAILER_AVAILABILITY_REDIS_CHANNEL, retailer_availabilities.to_json())  # type: ignore

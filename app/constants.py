import urllib.parse

import redis  # type: ignore

from app import settings
from app.models.ps5_version import PS5Version

if settings.REDIS_URL:
    urllib.parse.uses_netloc.append("redis")
    url = urllib.parse.urlparse(settings.REDIS_URL)

    HOST = url.hostname
    PORT = url.port
    PASSWORD = url.password
else:
    HOST = settings.REDIS_HOST
    PORT = settings.REDIS_PORT
    PASSWORD = None


RETAILER_REDIS_CONN = redis.Redis(host=HOST, port=PORT, password=PASSWORD)

RQ_REDIS_CONN = redis.Redis(host=HOST, port=PORT, password=PASSWORD)


TARGET_RETAILER = "Target"
BEST_BUY_RETAILER = "Best Buy"
NEW_EGG_RETAILER = "Newegg"
ADORAMA_RETAILER = "Adorama"
PLAYSTATION_DIRECT_RETAILER = "Playstation Direct"
GAMESTOP_RETAILER = "GameStop"
BH_RETAILER = "BH"

RETAILERS = [
    TARGET_RETAILER,
    BEST_BUY_RETAILER,
    NEW_EGG_RETAILER,
    ADORAMA_RETAILER,
    PLAYSTATION_DIRECT_RETAILER,
    GAMESTOP_RETAILER,
    BH_RETAILER,
]
PS5_VERSIONS = [PS5Version.DIGITAL, PS5Version.DISC]
PS5_DISC_MSRP = "499.99"
PS5_DIGITAL_MSRP = "399.99"
RETAILER_AVAILABILITY_REDIS_CHANNEL = "retailer-availability"
DEV_ENVIRONMENT = "development"
STAGING_ENVIRONMENT = "staging"
PRODUCTION_ENVIRONMENT = "production"

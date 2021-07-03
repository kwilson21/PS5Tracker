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

RETAILERS = [TARGET_RETAILER]
PS5_VERSIONS = [PS5Version.DIGITAL, PS5Version.DISC]

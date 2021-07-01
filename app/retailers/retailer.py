from abc import ABC
from abc import abstractmethod

from app.db.models import RetailerInfo
from app.models.availability import Availability
from app.models.ps5_version import PS5Version


class Retailer(ABC):
    @abstractmethod
    def get_availability(self, ps5_version: PS5Version) -> Availability:
        pass

    @abstractmethod
    def attempt_purchase(self, retailer_info: RetailerInfo, price: str) -> bool:
        pass

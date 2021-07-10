from typing import List

import orjson  # type: ignore
from pydantic import BaseModel

from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.stock_status import StockStatus


class Retailer(BaseModel):
    name: str
    availabilities: List[Availability]

    @property
    def in_stock_availabilities(self) -> List[Availability]:
        return [
            availability for availability in self.availabilities if availability.stock_status is StockStatus.IN_STOCK
        ]

    @property
    def versions_in_stock(self) -> List[PS5Version]:
        return [availability.version for availability in self.in_stock_availabilities]

    @classmethod
    def from_json(cls, data):
        return cls(**orjson.loads(data))

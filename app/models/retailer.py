from typing import List

import orjson  # type: ignore
from pydantic import BaseModel

from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.stock_status import StockStatus
from app.utils.json_utils import orjson_dumps


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

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

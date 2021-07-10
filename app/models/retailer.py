from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.stock_status import StockStatus


@dataclass_json
@dataclass(frozen=True, eq=True)
class Retailer:
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

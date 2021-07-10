from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json

from app.models.ps5_version import PS5Version
from app.models.stock_status import StockStatus


@dataclass_json
@dataclass(frozen=True, eq=True)
class Availability:
    version: PS5Version
    stock_status: StockStatus
    price: str
    updated_at: datetime

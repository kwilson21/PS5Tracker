from datetime import datetime

import orjson  # type: ignore
from pydantic import BaseModel

from app.models.ps5_version import PS5Version
from app.models.stock_status import StockStatus
from app.utils.json_utils import orjson_dumps


class Availability(BaseModel):
    version: PS5Version
    stock_status: StockStatus
    price: str
    updated_at: datetime

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

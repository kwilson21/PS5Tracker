from datetime import datetime

from pydantic import BaseModel

from app.models.ps5_version import PS5Version
from app.models.stock_status import StockStatus


class Availability(BaseModel):
    version: PS5Version
    stock_status: StockStatus
    price: str
    updated_at: datetime

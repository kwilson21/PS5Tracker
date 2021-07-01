from app.models.ps5_version import PS5Version
from app.models.stock_status import StockStatus


class Availability:
    version: PS5Version
    stock_status: StockStatus
    price: str

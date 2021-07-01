from typing import List

from app.models.availability import Availability


class Retailer:
    name: str
    availabilities: List[Availability]

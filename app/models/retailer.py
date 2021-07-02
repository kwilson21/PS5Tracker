from dataclasses import dataclass
from typing import List

from app.models.availability import Availability


@dataclass(frozen=True, eq=True)
class Retailer:
    name: str
    availabilities: List[Availability]

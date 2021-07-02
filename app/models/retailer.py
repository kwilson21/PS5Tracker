from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from app.models.availability import Availability


@dataclass_json
@dataclass(frozen=True, eq=True)
class Retailer:
    name: str
    availabilities: List[Availability]

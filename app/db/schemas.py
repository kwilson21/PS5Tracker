from datetime import datetime
from typing import Any
from typing import List
from typing import Optional

import orjson  # type: ignore
import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict

from app.utils.json_utils import orjson_dumps


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ConsolePreference(BaseModel):
    id: int  # noqa: A003
    ps5_version: str
    price: str
    retailer_info_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class RetailerInfoBase(BaseModel):
    name: str
    email: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class RetailerInfoCreate(RetailerInfoBase):
    password: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class RetailerInfo(RetailerInfoBase):
    id: int  # noqa: A003
    user_id: int
    console_preferences: List[ConsolePreference] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UserBase(BaseModel):
    email: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UserCreate(UserBase):
    password: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class User(UserBase):
    id: int  # noqa: A003
    phone_number: Optional[str]
    notify_by_sms: Optional[bool]
    notify_by_email: Optional[bool]
    notified_at: datetime
    is_active: bool
    retailer_info_items: List[RetailerInfo] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
        json_loads = orjson.loads
        json_dumps = orjson_dumps

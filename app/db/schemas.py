from typing import Any
from typing import List

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


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


class RetailerInfoBase(BaseModel):
    name: str
    email: str


class RetailerInfoCreate(RetailerInfoBase):
    password: str


class RetailerInfo(RetailerInfoBase):
    id: int  # noqa: A003
    user_id: int
    console_preferences: List[ConsolePreference] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int  # noqa: A003
    phone_number: str
    notify_by_sms: bool
    notify_by_email: bool
    is_active: bool
    retailer_info_items: List[RetailerInfo] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

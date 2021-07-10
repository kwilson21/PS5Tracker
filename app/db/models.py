from contextvars import ContextVar
from typing import Any
from typing import Dict
from typing import List

import peewee
from playhouse.db_url import connect

from app import settings
from app.constants import PS5_DIGITAL_MSRP
from app.constants import PS5_DISC_MSRP
from app.constants import RETAILERS
from app.models.ps5_version import PS5Version

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


if settings.DB_URL:
    mysql_db = connect(settings.DB_URL)
else:
    mysql_db = peewee.MySQLDatabase(
        settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASS, host=settings.DB_HOST, port=settings.DB_PORT
    )

mysql_db._state = PeeweeConnectionState()


class BaseModel(peewee.Model):
    class Meta:
        database = mysql_db


class User(BaseModel):
    email = peewee.CharField(unique=True)
    password = peewee.CharField()
    phone_number = peewee.CharField(unique=True)
    notify_by_sms = peewee.BooleanField()
    notify_by_email = peewee.BooleanField()
    is_active = peewee.BooleanField(default=True)


class RetailerInfo(BaseModel):
    name = peewee.CharField()
    email = peewee.CharField()
    password = peewee.CharField()
    user = peewee.ForeignKeyField(User, backref="retailer_info_items")


class ConsolePreference(BaseModel):
    ps5_version = peewee.CharField()
    price = peewee.CharField()
    retailer_info = peewee.ForeignKeyField(RetailerInfo, backref="console_preferences")


def add_user_and_base_preferences(
    email: str,
    phone_number: str,
    retailers: List[str] = RETAILERS,
    notify_by_sms: bool = False,
    notify_by_email: bool = False,
    console_preferences: List[Dict[str, Any]] = [  # noqa
        {"ps5_version": PS5Version.DIGITAL, "price": PS5_DIGITAL_MSRP},
        {"ps5_version": PS5Version.DISC, "price": PS5_DISC_MSRP},
    ],
):
    user = User.create(
        email=email,
        phone_number=phone_number,
        notify_by_sms=notify_by_sms,
        notify_by_email=notify_by_email,
    )

    user.save()

    for retailer_name in retailers:
        retailer_info = RetailerInfo.create(name=retailer_name, user=user)

        retailer_info.save()

        for cp in console_preferences:
            console_preference = ConsolePreference.create(
                ps5_version=cp["ps5_version"].value, price=cp["price"], retailer_info=retailer_info
            )

            console_preference.save()


def create_tables() -> None:
    mysql_db.create_tables([User, RetailerInfo, ConsolePreference])

    if settings.APP_ENV == "development":
        add_user_and_base_preferences(
            email=settings.TEST_EMAIL,
            phone_number=settings.TEST_PHONE_NUMBER,
            notify_by_sms=bool(settings.TEST_PHONE_NUMBER),
            notify_by_email=bool(settings.TEST_EMAIL),
        )


def drop_tables() -> None:
    if settings.APP_ENV == "development":
        mysql_db.drop_tables([User, RetailerInfo, ConsolePreference])

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import fakeredis
import pytest
from pytest_mock import MockerFixture

from app.constants import TARGET_RETAILER
from app.db import retailer_store
from app.models.availability import Availability
from app.models.ps5_version import PS5Version
from app.models.retailer import Retailer
from app.models.stock_status import StockStatus


@pytest.fixture
def retailer() -> Retailer:
    return Retailer(
        name=TARGET_RETAILER,
        availabilities=[
            Availability(
                version=PS5Version.DIGITAL,
                stock_status=StockStatus.OUT_OF_STOCK,
                price="399.99",
                updated_at=datetime(2021, 1, 1, tzinfo=timezone(timedelta(days=-1, seconds=68400))),
            )
        ],
    )


def test_update_retailer_availabilities(mocker: MockerFixture, retailer: Retailer) -> None:
    r = fakeredis.FakeStrictRedis()
    mocker.patch("app.db.retailer_store.RETAILER_REDIS_CONN", r)

    result = retailer_store.update_retailer_availabilities(retailer)

    assert result is True
    assert r.get(retailer.name).decode("utf-8") == retailer.json()  # type: ignore


def test_get_all_retailer_availabilities(mocker: MockerFixture, retailer: Retailer) -> None:
    r = fakeredis.FakeStrictRedis()
    mocker.patch("app.db.retailer_store.RETAILER_REDIS_CONN", r)

    r.set(retailer.name, retailer.json())  # type: ignore

    result = retailer_store.get_all_retailer_availabilities()

    assert result == [retailer]  # type: ignore


def test_get_retailer_availability(mocker: MockerFixture, retailer: Retailer) -> None:
    r = fakeredis.FakeStrictRedis()
    mocker.patch("app.db.retailer_store.RETAILER_REDIS_CONN", r)

    r.set(retailer.name, retailer.json())  # type: ignore

    result = retailer_store.get_retailer_availability(TARGET_RETAILER)

    assert result == retailer


def test_delete_retailer_availability(mocker: MockerFixture, retailer: Retailer) -> None:
    r = fakeredis.FakeStrictRedis()
    mocker.patch("app.db.retailer_store.RETAILER_REDIS_CONN", r)

    r.set(retailer.name, retailer.json())  # type: ignore

    result = retailer_store.delete_retailer_availability(TARGET_RETAILER)

    assert result is True
    assert r.get(retailer.name) is None


def test_delete_all_retailer_availabilities(mocker: MockerFixture, retailer: Retailer) -> None:
    r = fakeredis.FakeStrictRedis()
    mocker.patch("app.db.retailer_store.RETAILER_REDIS_CONN", r)

    r.set(retailer.name, retailer.json())  # type: ignore

    result = retailer_store.delete_all_retailer_availabilities()

    assert result is True
    assert r.get(retailer.name) is None

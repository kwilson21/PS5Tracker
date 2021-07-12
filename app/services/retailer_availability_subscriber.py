import time
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List

import gevent

from app.constants import RETAILER_AVAILABILITY_REDIS_CHANNEL
from app.constants import RETAILER_REDIS_CONN
from app.db.models import ConsolePreference
from app.models.retailer import Retailer as RetailerModel
from app.services import notifications


def _retailer_availability_handler(message: Dict[str, bytes]) -> None:
    print(f"Recieved {message=}")
    if isinstance(message, dict):
        _message = message
    else:
        return

    if isinstance(_message["data"], int):
        return

    retailer = RetailerModel.from_json(_message["data"])  # type: ignore

    if not retailer.in_stock_availabilities:
        return

    phone_numbers: List[str] = []
    emails: List[str] = []

    for console_preference in ConsolePreference.select().where(
        ConsolePreference.ps5_version << [v.value for v in retailer.versions_in_stock]
    ):
        notified_at = console_preference.retailer_info.user.notified_at
        notified_time_ok = (datetime.utcnow() - notified_at) > timedelta(days=1)

        if console_preference.retailer_info.user.notify_by_sms and notified_time_ok:
            console_preference.retailer_info.user.notified_at = datetime.utcnow()
            phone_numbers.append(console_preference.retailer_info.user.phone_number)
        if console_preference.retailer_info.user.notify_by_email and notified_time_ok:
            console_preference.retailer_info.user.notified_at = datetime.utcnow()
            emails.append(console_preference.retailer_info.user.email)

    for phone_number in phone_numbers:
        gevent.spawn(notifications.sms_retailer_availabilities, retailer, phone_number)

    for email in emails:
        gevent.spawn(notifications.email_retailer_availabilities, email)


subscriber = RETAILER_REDIS_CONN.pubsub()

subscriber.psubscribe(**{RETAILER_AVAILABILITY_REDIS_CHANNEL: _retailer_availability_handler})


def listen_for_messages() -> None:
    while True:
        message = subscriber.get_message(ignore_subscribe_messages=True)
        if message:
            _retailer_availability_handler(message)
        time.sleep(0.001)

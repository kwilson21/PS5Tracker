from typing import List

import gevent

from app.constants import RETAILER_AVAILABILITY_REDIS_CHANNEL
from app.constants import RETAILER_REDIS_CONN
from app.db.models import ConsolePreference
from app.models.retailer import Retailer as RetailerModel
from app.services import notifications


def _retailer_availability_handler(message: str) -> None:
    retailer = RetailerModel.from_json(message["data"])  # type: ignore

    if not retailer.in_stock_availabilities:
        return

    phone_numbers: List[str] = []
    emails: List[str] = []

    for console_preference in ConsolePreference.select().where(
        ConsolePreference.ps5_version << [v.value for v in retailer.versions_in_stock]
    ):
        if console_preference.retailer_info.user.notify_by_sms:
            phone_numbers.append(console_preference.retailer_info.user.phone_number)
        if console_preference.retailer_info.user.notify_by_email:
            emails.append(console_preference.retailer_info.user.email)

    while phone_numbers[:]:
        numbers_to_text, phone_numbers = phone_numbers[:300], phone_numbers[300:]
        gevent.spawn(notifications.sms_retailer_availabilities, retailer, numbers_to_text)

    for email in emails:
        gevent.spawn(notifications.email_retailer_availabilities, email)


subscriber = RETAILER_REDIS_CONN.pubsub()

subscriber.psubscribe(**{RETAILER_AVAILABILITY_REDIS_CHANNEL: _retailer_availability_handler})

thread = subscriber.run_in_thread(sleep_time=0.001)

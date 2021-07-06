import json
from typing import Any
from typing import Dict
from typing import List

import gevent

from app.constants import RETAILER_AVAILABILITY_REDIS_CHANNEL
from app.constants import RETAILER_REDIS_CONN
from app.db.models import ConsolePreference
from app.models.retailer import Retailer as RetailerModel
from app.services import notifications


def _retailer_availability_handler(message: Dict[str, Any]) -> None:
    retailer_availabilities = json.loads(message["data"])
    for _retailer in retailer_availabilities:
        try:
            retailer = RetailerModel.from_dict(_retailer)  # type: ignore
        except AttributeError:
            print(message["data"])
            print(retailer)
            raise

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

        for phone_number in phone_numbers:
            gevent.spawn(notifications.sms_retailer_availabilities, retailer, phone_number)

        for email in emails:
            gevent.spawn(notifications.email_retailer_availabilities, email)


subscriber = RETAILER_REDIS_CONN.pubsub()

subscriber.psubscribe(**{RETAILER_AVAILABILITY_REDIS_CHANNEL: _retailer_availability_handler})

thread = subscriber.run_in_thread(sleep_time=0.001)

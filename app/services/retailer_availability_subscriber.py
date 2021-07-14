import time
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List

import gevent

from app.constants import RETAILER_AVAILABILITY_REDIS_CHANNEL
from app.constants import RETAILER_REDIS_CONN
from app.db.models import ConsolePreference
from app.db.models import RetailerInfo
from app.db.models import User
from app.models.retailer import Retailer as RetailerModel
from app.services import notifications
from app.settings import NOTIFICATIONS_COOLDOWN_TIME


def _retailer_availability_handler(message: Dict[str, bytes]) -> None:
    print(f"Recieved {message=}")
    if isinstance(message, dict):
        _message = message
    else:
        return

    if isinstance(_message["data"], int):
        return

    retailer = RetailerModel.parse_raw(_message["data"])

    if not retailer.in_stock_availabilities:
        return

    phone_numbers: List[str] = []
    emails: List[str] = []

    query = (
        User.select()
        .join(RetailerInfo)
        .join(ConsolePreference)
        .where(
            (User.notify_by_sms == True | User.notify_by_email == True)  # noqa: E712
            and (RetailerInfo.name == retailer.name)
            and ConsolePreference.ps5_version << [v.value for v in retailer.versions_in_stock]
        )
        .group_by(User)
    )

    for user in query:
        notified_at = user.notified_at
        notified_time_ok = (datetime.utcnow() - notified_at) > timedelta(minutes=NOTIFICATIONS_COOLDOWN_TIME)

        if user.notify_by_sms and notified_time_ok:
            user.notified_at = datetime.utcnow()
            user.save()
            phone_numbers.append(user.phone_number)
        if user.notify_by_email and notified_time_ok:
            user.notified_at = datetime.utcnow()
            user.save()
            emails.append(user.email)

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

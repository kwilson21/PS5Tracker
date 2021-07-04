from typing import List

import gevent

from app.constants import RETAILER_AVAILABILITY_REDIS_CHANNEL
from app.constants import RETAILER_REDIS_CONN
from app.db.models import User
from app.models.ps5_version import PS5Version
from app.models.retailer import Retailer as RetailerModel
from app.services.email_availability_notification import email_retailer_availabilities
from app.services.sms_availability_notification import sms_retailer_availabilities


def _retailer_availability_handler(message: str) -> None:
    retailer = RetailerModel.from_json(message["data"])  # type: ignore

    if not retailer.in_stock_availabilities:
        return

    phone_numbers: List[str] = []
    emails: List[str] = []

    for retailer_info in User.retailer_info:
        for console_preference in retailer_info.console_preferences:
            if PS5Version[console_preference.ps5_version] in retailer.versions_in_stock:
                if retailer_info.user.notify_by_sms:
                    phone_numbers.append(retailer_info.user.phone_number)
                if retailer_info.user.notify_by_email:
                    emails.append(retailer_info.user.email)

    sms_jobs: gevent.Greenlet = []
    email_jobs: gevent.Greenlet = []

    while phone_numbers[:]:
        numbers_to_text, phone_numbers = phone_numbers[:300], phone_numbers[300:]
        sms_jobs.append(gevent.spawn(sms_retailer_availabilities, retailer, numbers_to_text))

    for email in emails:
        email_jobs.append(gevent.spawn(email_retailer_availabilities, email))

    for email_job in email_jobs:
        email_job.join()

    for sms_job in sms_jobs:
        sms_job.join()


subscriber = RETAILER_REDIS_CONN.pubsub()

subscriber.psubscribe(**{RETAILER_AVAILABILITY_REDIS_CHANNEL: _retailer_availability_handler})

thread = subscriber.run_in_thread(sleep_time=0.001)

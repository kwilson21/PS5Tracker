from typing import List

import gevent
import requests  # type: ignore
import settings

from app.constants import RETAILER_AVAILABILITY_REDIS_CHANNEL
from app.constants import RETAILER_REDIS_CONN
from app.db.models import User
from app.models.ps5_version import PS5Version
from app.models.retailer import Retailer as RetailerModel


def _email_retailer_availabilities(email: str) -> None:
    pass


def _text_retailer_availabilities(retailer: RetailerModel, numbers_to_text: List[str]) -> None:
    text_str = f"{retailer.name} has PS5 versions in stock!"
    responses: List[str] = []

    for availability in retailer.in_stock_availabilities:
        text_str += f"\nVERSION: {availability.version.value} PRICE: {availability.price}"
        responses.append(f"Purchase {availability.version.value}")

    text_str += "\nWould you like to attempt to automatically purchase a console?"

    requests.post(
        settings.TILL_URL,
        json={
            "phone": numbers_to_text,
            "method": "SMS",
            "questions": [
                {
                    "text": text_str,
                    "tag": "retailer_availability",
                    "responses": responses + ["Do not purchase"],
                    "webhook": f"{settings.URL}/purchase-attempt-sms-response",
                }
            ],
        },
    )


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

    sms_jobs = []
    email_jobs = []

    while phone_numbers[:]:
        numbers_to_text, phone_numbers = phone_numbers[:300], phone_numbers[300:]
        sms_jobs.append(gevent.spawn(_text_retailer_availabilities, retailer, numbers_to_text))

    for email in emails:
        email_jobs.append(gevent.spawn(_email_retailer_availabilities, email))

    for email_job in email_jobs:
        email_job.join()

    for sms_job in sms_jobs:
        sms_job.join()


subscriber = RETAILER_REDIS_CONN.pubsub()

subscriber.psubscribe(**{RETAILER_AVAILABILITY_REDIS_CHANNEL: _retailer_availability_handler})

thread = subscriber.run_in_thread(sleep_time=0.001)

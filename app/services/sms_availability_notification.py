from typing import List

import requests  # type: ignore

from app import settings
from app.models.retailer import Retailer as RetailerModel


def sms_retailer_availabilities(retailer: RetailerModel, numbers_to_text: List[str]) -> None:
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

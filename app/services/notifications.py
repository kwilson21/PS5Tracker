from typing import List

from twilio.rest import Client

from app import settings
from app.models.retailer import Retailer as RetailerModel

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def sms_retailer_availabilities(retailer: RetailerModel, phone_number: str) -> None:
    text_str = f"{retailer.name} has PS5 versions in stock!\n"
    responses: List[str] = []

    for availability in retailer.in_stock_availabilities:
        text_str += f"\nVersion: {availability.version.value}"
        text_str += " " * 6
        text_str += f"\nPrice: ${availability.price}"
        responses.append(f"Purchase {availability.version.value}")

    text_str += "\n\nWould you like to attempt to automatically purchase a console?"
    text_str += '\n\nReply with "Yes" or "No"'

    client.messages.create(
        body=text_str,
        from_="+17708572635",
        status_callback=f"{settings.URL}/purchase-attempt-sms-response",
        to=phone_number,
    )


def email_retailer_availabilities(email: str) -> None:
    pass

from gevent import monkey  # isort:skip # noqa

monkey.patch_all()  # isort:skip # noqa

from app.services.retailer_availability_subscriber import listen_for_messages  # noqa

if __name__ == "__main__":
    listen_for_messages()

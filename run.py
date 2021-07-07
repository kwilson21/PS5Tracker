from gevent import monkey  # isort:skip # noqa

monkey.patch_all()  # isort:skip # noqa

from app.app import app  # noqa

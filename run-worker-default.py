from gevent import monkey  # isort:skip # noqa

monkey.patch_all()  # isort:skip # noqa

from rq import Connection  # noqa
from rq import Queue  # noqa
from rq.worker import HerokuWorker as Worker  # noqa

from app.constants import RQ_REDIS_CONN  # noqa

if __name__ == "__main__":
    with Connection(RQ_REDIS_CONN):
        worker = Worker(Queue(default_timeout=75), default_result_ttl=0)
        worker.work()

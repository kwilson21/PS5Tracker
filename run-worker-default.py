from rq import Connection
from rq import Queue
from rq.worker import HerokuWorker as Worker

from app.constants import RQ_REDIS_CONN

if __name__ == "__main__":
    with Connection(RQ_REDIS_CONN):
        worker = Worker(Queue("default"))
        worker.work()

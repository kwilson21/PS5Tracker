from datetime import datetime

from rq_scheduler import Scheduler

from app.constants import RQ_REDIS_CONN
from app.rq.jobs import all_jobs

scheduler = Scheduler(connection=RQ_REDIS_CONN)


def schedule_periodic_jobs():
    for job in all_jobs:
        scheduler.schedule(scheduled_time=datetime.utcnow(), func=job, interval=1200)  # Run every 30 minutes

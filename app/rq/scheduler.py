from datetime import datetime

from rq_scheduler import Scheduler

from app.constants import PERIODIC_JOB_TIME_INTERVAL
from app.constants import RETAILERS
from app.constants import RQ_REDIS_CONN
from app.rq.jobs import update_retailer_availabilities

scheduler = Scheduler(connection=RQ_REDIS_CONN)


def schedule_periodic_jobs() -> None:
    for retailer_name in RETAILERS:
        scheduler.schedule(
            scheduled_time=datetime.utcnow(),
            func=update_retailer_availabilities,
            args=[retailer_name],
            interval=PERIODIC_JOB_TIME_INTERVAL,
            timeout=240,
        )


def clear_all_jobs() -> None:
    [scheduler.cancel(job) for job in scheduler.get_jobs()]

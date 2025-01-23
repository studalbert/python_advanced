from random import random
import logging
from celery import Celery
from celery.schedules import crontab

app = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)

app.conf.broker_connection_retry_on_startup = True

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, check_cat.s(), name="check every 20 sec")
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        check_cat.s(),
        name="check at 7-30 on Monday",
    )


@app.task
def check_cat():
    if random() < 0.5:
        logger.info("Кот ничего не сломал.")
    else:
        logger.info("Кот что-то сломал...")

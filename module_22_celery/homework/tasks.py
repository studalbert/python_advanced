"""
В этом файле будут Celery-задачи
"""

from celery import Celery
from celery.schedules import crontab
from image import blur_image
from mail import send_email, send_email_weakly
from model import session, User
import os

celery_app = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)

celery_app.conf.broker_connection_retry_on_startup = True


@celery_app.task
def task_blur_image(image):
    blur_image(image)


@celery_app.task
def task_send_email_weakly():
    users = session.query(User).all()
    for user in users:
        send_email_weakly(receiver=user.email)


@celery_app.task
def task_send_email(user_email: str, *args):
    send_email(receiver=user_email, filename="blurred_images.zip")


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=12, minute=0, day_of_week="mon"),
        task_send_email_weakly.s(),
        name="send_email_weekly",
    )

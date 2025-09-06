from flask import Flask

from app.extensions import scheduler
from .remove_sponsor import remove_users_sponsorships_expired


def init(app: Flask) -> None:
    scheduler.add_job(
        id = 'remove_expired_sponsorships',
        func = lambda: remove_users_sponsorships_expired(app),
        trigger = 'interval',
        minutes = 3,
        misfire_grace_time = 30
    )
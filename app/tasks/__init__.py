from flask_apscheduler import APScheduler

from .update_prices import update_crypto_prices


def register_tasks(scheduler: APScheduler, app):
    scheduler.add_job(
        id="update_prices",
        func=lambda: update_crypto_prices(app),
        trigger="interval",
        hours=1
    )
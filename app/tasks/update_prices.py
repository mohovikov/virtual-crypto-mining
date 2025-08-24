from flask import Flask

from app import services, helpers
from app.extensions import db


def update_crypto_prices(app: Flask):
    with app.app_context():
        try:
            cryptos = services.get_all_cryptocurrencies()
            for crypto in cryptos:
                price = helpers.generate_price()
                services.add_crypto_price_history(crypto.id, price)
                crypto.price = price
            db.session.commit()

            count = len(cryptos)

            services.add_scheduler_log(
                job_name="update_prices",
                message=f"Для {count} {'монеты' if count == 1 else 'монет'} обновлен курс"
            )
        except Exception as e:
            db.session.rollback()
            services.add_scheduler_log(
                job_name="update_prices",
                is_success=False,
                message=str(e)
            )
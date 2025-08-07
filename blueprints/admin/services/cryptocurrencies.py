import requests
from core import db
from core.config import Config
from core.models import CryptoCurrencies
from core.utils import download_coin_icon


CRYPTOCURRENCIES_PER_PAGE = 25

def get_all_cryptocurrencies():
    return CryptoCurrencies.query.all()

def get_cryptocurrencies_paginated(page: int = 1):
    return CryptoCurrencies.query.order_by(CryptoCurrencies.id.asc()).paginate(page=page, per_page=CRYPTOCURRENCIES_PER_PAGE)

def load_cryptocurrencies():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": Config.CMC_API_KEY}
    params = {"convert": "RUB", "cryptocurrency_type": "coins", "price_min": 0.01}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()["data"]

        for coin in data:
            id = coin["id"]
            name = coin["name"]
            symbol = coin["symbol"]
            price = coin["quote"]["RUB"]["price"]
            icon_url = f"https://s2.coinmarketcap.com/static/img/coins/64x64/{coin['id']}.png"

            # Пропуск если уже есть
            if CryptoCurrencies.query.filter_by(name=name, symbol=symbol).first():
                continue

            icon_file = download_coin_icon(icon_url, name)
            db.session.add(CryptoCurrencies(
                cid=id,
                name=name,
                symbol=symbol,
                icon_name=icon_file,
                price=price
            ))

        db.session.commit()
        return "Монеты успешно добавлены!", "success"

    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при получении монет: {ex}", "danger"
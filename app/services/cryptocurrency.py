from app.extensions import db
from app.forms import admin_forms as forms
from app.helpers import save_cryptocurrency_hashed_file, generate_price
from app.models import Cryptocurrency, CryptoPriceHistory


def get_all_cryptocurrencies():
    return Cryptocurrency.query.all()

def get_cryptocurrency(crypto_id: int):
    return Cryptocurrency.query.get(crypto_id)

def create_cryptocurrency(form: forms.ManageCryptocurrencyForm, is_approved: bool = True, creator_id: int = -1) -> tuple[bool, str, str]:
    cryptocurrency = Cryptocurrency(
        name = str(form.name.data),
        symbol = str(form.symbol.data),
        price = 0.00,
        is_approved = is_approved,
        creator_id = 999 if creator_id == -1 else creator_id
    )
    try:
        db.session.add(cryptocurrency)
        db.session.flush()

        if hasattr(form, "icon_file") and form.icon_file.data:
            cryptocurrency.icon_file = save_cryptocurrency_hashed_file(cryptocurrency.id, form.icon_file.data, "icon")

        db.session.commit()
        return True, f"Криптовалюта «{form.name.data}» успешно добавлена", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при добавлении:<br>{ex}", "danger"

def edit_cryptocurrency(cryptocurrency: Cryptocurrency | None, form: forms.ManageCryptocurrencyForm) -> tuple[bool, str, str]:
    if not cryptocurrency:
        return False, "Монеты с таким ID не найдено", "warning"

    try:
        cryptocurrency.name = str(form.name.data)
        cryptocurrency.symbol = str(form.symbol.data)

        if hasattr(form, "icon_file") and form.icon_file.data:
            cryptocurrency.icon_file = save_cryptocurrency_hashed_file(cryptocurrency.id, form.icon_file.data, "icon")

        db.session.commit()
        return True, f"Криптовалюта «{form.name.data}» успешно изменена", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при изменении:<br>{ex}", "danger"

def update_price_cryptocurrency(crypto_id: int) -> tuple[str, str]:
    cryptocurrency = get_cryptocurrency(crypto_id)

    if not cryptocurrency:
        return "Криптовалюты с таким ID не найдено", "warning"

    try:
        new_price = generate_price()
        cryptocurrency.price = new_price

        add_crypto_price_history(cryptocurrency.id, new_price)

        return f"Курс для монеты «{cryptocurrency.name}» обновлен!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при обновлении курса:<br>{ex}", "danger"

def add_crypto_price_history(crypto_id, price):
    db.session.add(CryptoPriceHistory(
        crypto_id=crypto_id,
        price=price
    ))
    db.session.commit()

    history = (CryptoPriceHistory.query
            .filter_by(crypto_id=crypto_id)
            .order_by(CryptoPriceHistory.created_at.desc())
            .all())

    if len(history) > 50:
        for entry in history[50:]:  # берём все кроме первых 15
            db.session.delete(entry)
        db.session.commit()
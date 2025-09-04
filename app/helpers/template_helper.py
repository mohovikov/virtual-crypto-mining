from babel import Locale

from flask_babel import get_locale
from flask import request
from flask_login import current_user

from app.constants.privileges import Privileges


def get_version() -> str:
    try:
        with open("version", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "unknown"

def get_country_choices():
    """Возвращает список стран в зависимости от текущей локали"""
    locale = Locale.parse(str(get_locale()) or 'en')
    countries = locale.territories

    choices = [(code, name) for code, name in countries.items() if len(code) == 2]
    choices.sort(key=lambda x: x[1])
    return choices

def get_privileges_list(user_privileges: int, gd: bool) -> list[dict[str, str]]:
    privileges_list: list = []

    for privilege in Privileges:
        if privilege.value <= 0:
            continue
        
        privileges_list.append({
            "name": privilege.name,
            "value": privilege.value,
            "checked": "checked" if (user_privileges & privilege.value) > 0 else "",
            "disabled": "disabled" if (privilege.value <= 2 and not gd) else "",
            "gd": "disabled" if gd else False
        })
    return privileges_list

def is_active(endpoint):
    return "active" if request.endpoint == endpoint else ""

def is_active_prefix(prefix):
    return "active" if str(request.endpoint).startswith(prefix) else ""
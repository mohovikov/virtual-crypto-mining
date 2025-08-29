from babel import Locale

from flask_babel import get_locale
from flask import request


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

def is_active(endpoint):
    return "active" if request.endpoint == endpoint else ""

def is_active_prefix(prefix):
    return "active" if str(request.endpoint).startswith(prefix) else ""
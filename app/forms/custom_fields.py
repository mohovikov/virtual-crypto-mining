from wtforms import SelectField
from flask_babel import get_locale
from babel import Locale


class CountrySelectField(SelectField):
    def __init__(self, label=None, validators=None, **kwargs):
        locale = Locale(str(get_locale()))
        choices = [(code, name) for code, name in locale.territories.items() if len(code) == 2]
        choices.sort(key=lambda x: x[1])

        super().__init__(label, validators, choices=choices, **kwargs)
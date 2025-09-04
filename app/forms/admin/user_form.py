from flask_wtf import FlaskForm
import wtforms as forms
import wtforms.validators as validators

from app.helpers.template_helper import get_country_choices


class SettingsForm(FlaskForm):
    id = forms.IntegerField(
        label = "ID",
        validators = [
            validators.DataRequired()
        ],
        render_kw = {
            "class": "form-control",
            "readonly": True
        }
    )
    username = forms.StringField(
        label = "Имя пользователя",
        validators = [
            validators.DataRequired()
        ],
        render_kw = {
            "class": "form-control",
            "readonly": True
        }
    )
    username_aka = forms.StringField(
        label = "Дополнительный никнейм (a.k.a)",
        validators = [
            validators.DataRequired()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    email = forms.EmailField(
        label = "Email",
        validators = [
            validators.DataRequired(),
            validators.Email()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    country = forms.SelectField(
        label = "Страна",
        validators = [
            validators.DataRequired()
        ],
        choices = get_country_choices,
        validate_choice = False
    )
    userpage = forms.TextAreaField(
        label = "Страница пользователя",
        validators = [
            validators.Optional()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    privileges_value = forms.IntegerField(
        label = "Значение привилегий",
        validators = [
            validators.DataRequired()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
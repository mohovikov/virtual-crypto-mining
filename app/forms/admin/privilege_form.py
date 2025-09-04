from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField
from wtforms.validators import DataRequired


class PrivilegeForm(FlaskForm):
    name = StringField(
        label = "Название",
        validators = [
            DataRequired()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    privileges_value = IntegerField(
        label = "Значение привилегий",
        validators = [DataRequired()],
        render_kw = {
            "class": "form-control"
        }
    )
    color = SelectField(
        label = "Цвет",
        validators = [DataRequired()],
        choices = (
            ('primary', 'Синий'),
            ('secondary', 'Серый'),
            ('success', 'Зеленый'),
            ('danger', 'Красный'),
            ('warning', 'Желтый'),
            ('info', 'Голубой'),
            ('light', 'Белый'),
            ('dark', 'Черный'),
        )
    )
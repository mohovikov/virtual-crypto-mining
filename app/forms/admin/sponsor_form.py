from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class SponsorAwardForm(FlaskForm):
    amount = IntegerField(
        label = "Срок действия",
        validators = [
            DataRequired(),
            NumberRange(min = 1, max = 240, message="Срок должен быть от 1 до 240 месяцев")
        ],
        render_kw = {
            "class": "form-control",
            "min": 1,
            "max": 240,
            "value": 1
        }
    )
    type = SelectField(
        "Единица измерения",
        choices = [
            ("add", "Добавить месяц"),
            ("remove", "Убрать месяц"),
        ],
        validators = [DataRequired()],
        render_kw = {
            "class": "form-select"
        }
    )
    submit = SubmitField("Выдать / продлить спонсорство")
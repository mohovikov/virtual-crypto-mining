from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, Email

from app.config import Config


class AddPrivilegeGroup(FlaskForm):
    name = StringField(
        "Название",
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    color_class = SelectField("Цвет", choices=(
        ("primary", "Синий"),
        ("secondary", "Серый"),
        ("success", "Зеленый"),
        ("danger", "Красный"),
        ("warning", "Желтый"),
        ("info", "Голубой"),
        ("light", "Белый"),
        ("dark", "Черный")
    ))
    privileges_value = IntegerField(
        "Значение группы привилегии",
        default=3,
        render_kw={"min": 3},
        validators=[DataRequired()]
    )
    submit = SubmitField("Создать привилегию")

class EditUserForm(FlaskForm):
    id = IntegerField("ID", render_kw={"class": "form-control-plaintext", "readonly": True})
    username = StringField("Имя пользователя", render_kw={"class": "form-control"})
    username_aka = StringField("A.K.A", render_kw={"class": "form-control"})
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"}
    )
    userpage = TextAreaField("Раздел 'О себе'")
    privileges_value = IntegerField(
        "Значение группы привилегии",
        render_kw={"min": 3, "class": "form-control"},
        validators=[DataRequired()]
    )
    country = SelectField("Страна")
    submit = SubmitField("Сохранить изменения")

class GiveSponsorForm(FlaskForm):
    id = IntegerField("ID", render_kw={"class": "form-control-plaintext", "readonly": True})
    username = StringField("Имя пользователя", render_kw={"class": "form-control-plaintext", "readonly": True})
    amount = IntegerField("Длительность", default=1, render_kw={"class": "form-control", "min": 1}, validators=[DataRequired()])
    unit = SelectField(choices=(
        ("hours", f"Часы (макс. {Config.SPONSOR_LIMITS['hours']})"),
        ("days", f"Дни (макс. {Config.SPONSOR_LIMITS['days']})"),
        ("months", f"Месяцы (макс. {Config.SPONSOR_LIMITS['months']})"),
        ("years", f"Годы (макс. {Config.SPONSOR_LIMITS['years']})"),
    ), validators=[DataRequired()])
    submit = SubmitField("Выдать \"Спонсора\"", render_kw={"class": "btn btn-sm btn-primary"})

    def validate_amount(self, field):
        unit = self.unit.data
        if unit not in Config.SPONSOR_LIMITS:
            raise ValidationError("Неверная единица времени")
        if field.data <= 0 or field.data > Config.SPONSOR_LIMITS[unit]:
            raise ValidationError(f"Максимум для {unit} — {Config.SPONSOR_LIMITS[unit]}")
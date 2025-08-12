from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


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
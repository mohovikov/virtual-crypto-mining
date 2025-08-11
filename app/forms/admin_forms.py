from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


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
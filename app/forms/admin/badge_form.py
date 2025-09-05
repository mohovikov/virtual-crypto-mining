from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import ListWidget, CheckboxInput


class BadgeForm(FlaskForm):
    name = StringField(
        label = "Название",
        validators = [
            DataRequired()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    description = StringField(
        label = "Описание",
        validators = [
            Optional()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    icon = StringField(
        label = "Иконка",
        validators = [
            DataRequired()
        ],
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

class MultiCheckboxField(SelectMultipleField):
    """Кастомное поле с чекбоксами вместо обычного select."""
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist
        else:
            self.data = []

class UserBadgesForm(FlaskForm):
    badges = MultiCheckboxField("Выберите бейджи", validators=[Optional()])
    submit = SubmitField("Сохранить")
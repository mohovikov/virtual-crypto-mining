from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, NumberRange, DataRequired, Email


class SponsorForm(FlaskForm):
    user_id = IntegerField("ID пользователя", render_kw={"readonly": True, "class": "form-control-plaintext"})
    username = StringField("Имя пользователя", render_kw={"readonly": True, "class": "form-control-plaintext"})

    duration = IntegerField("Время действия", validators=[
        InputRequired(),
        NumberRange(min=1, max=8760)  # макс 1 год в часах
    ], render_kw={"class": "form-control", "value": 1})
    unit = SelectField("Единица времени", choices=[
        ('hours', 'Час(ов)'),
        ('days', 'День(дней)'),
        ('months', 'Месяц(ев)'),
        ('years', 'Год(лет)')
    ], validators=[InputRequired()], render_kw={"class": "form-select"})

    submit = SubmitField("Выдать спонсорство", render_kw={"class": "btn btn-primary"})

class UserEditForm(FlaskForm):
    id = IntegerField("ID пользователя", render_kw={"readonly": True, "class": "form-control-plaintext"})
    username = StringField("Имя пользователя", render_kw={"class": "form-control"})
    username_aka = StringField("A.K.A", render_kw={"class": "form-control"})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    userpage = TextAreaField("Раздел \"Информация\"", render_kw={"class": "form-control"})
    privileges = IntegerField("Значение привелегий", render_kw={"id": "privileges-value"})
    country = StringField("Страна", render_kw={"class": "form-control"})

    submit = SubmitField("Сохранить изменения", render_kw={"class": "btn btn-primary"})
from flask_wtf import FlaskForm
import wtforms as forms
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models.users import User


class RegisterForm(FlaskForm):
    username = forms.StringField(
        "Имя пользователя",
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = forms.StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = forms.PasswordField(
        "Пароль",
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = forms.PasswordField(
        "Подтверждение пароля",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = forms.SubmitField("Зарегистрироваться")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise forms.ValidationError("Это имя уже занято.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise forms.ValidationError("Этот email уже зарегистрирован.")

class LoginForm(FlaskForm):
    username = forms.StringField(
        "Имя пользователя",
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    password = forms.PasswordField(
        "Пароль",
        validators=[DataRequired()]
    )
    remember = forms.BooleanField("Запомнить меня")
    submit = forms.SubmitField("Войти")

class ClanCreateForm(FlaskForm):
    name = forms.StringField("Название клана", validators=[DataRequired(), Length(max=255)], render_kw={"class": "form-control"})
    short_name = forms.StringField("Тэг клана", validators=[DataRequired(), Length(max=255)], render_kw={"class": "form-control"})
    is_open = forms.BooleanField("Открытый набор", default=True)
    submit = forms.SubmitField("Создать клан", render_kw={"class": "btn btn-sm btn-primary"})

class ClanSettingsForm(FlaskForm):
    name = forms.StringField("Название клана", render_kw={"class": "form-control"})
    short_name = forms.StringField("Тэг клана", render_kw={"class": "form-control"})
    is_open = forms.RadioField("Открытый набор", choices=[('1', 'Да'), ('0', 'Нет')])
    logo_file = FileField("Загрузка аватарки", render_kw={"class": "form-control"})
    banner_file = FileField("Загрузка обложки", render_kw={"class": "form-control"})
    url = forms.URLField("Ссылка клана", render_kw={"class": "form-control"})
    description = forms.TextAreaField("Описание клана", render_kw={"class": "form-control"})
    submit = forms.SubmitField("Сохранить изменения", render_kw={"class": "btn btn-sm btn-primary"})
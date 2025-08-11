from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models.users import Users


class RegisterForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        "Подтверждение пароля",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Зарегистрироваться")

    def validate_username(self, username):
        if Users.query.filter_by(username=username.data).first():
            raise ValidationError("Это имя уже занято.")

    def validate_email(self, email):
        if Users.query.filter_by(email=email.data).first():
            raise ValidationError("Этот email уже зарегистрирован.")

class LoginForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired()]
    )
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
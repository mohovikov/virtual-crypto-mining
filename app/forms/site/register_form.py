from flask_wtf import FlaskForm
import wtforms as forms
import wtforms.validators as validators

from app.models import User


class RegisterForm(FlaskForm):
    username = forms.StringField(
        "Имя пользователя",
        validators=[validators.DataRequired(), validators.Length(min=3, max=20)]
    )
    email = forms.StringField(
        "Email",
        validators=[validators.DataRequired(), validators.Email()]
    )
    password = forms.PasswordField(
        "Пароль",
        validators=[validators.DataRequired(), validators.Length(min=8)]
    )
    confirm_password = forms.PasswordField(
        "Подтверждение пароля",
        validators=[validators.DataRequired(), validators.EqualTo("password")]
    )
    submit = forms.SubmitField("Зарегистрироваться")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise forms.ValidationError("Это имя уже занято.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
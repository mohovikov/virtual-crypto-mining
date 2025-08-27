from flask_wtf import FlaskForm
import wtforms as forms
import wtforms.validators as validators

from app.models import User


class RegisterForm(FlaskForm):
    username = forms.StringField(
        "Имя пользователя",
        validators=[
            validators.DataRequired(),
            validators.Length(min=3, max=32)
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    email = forms.EmailField(
        "Email",
        validators=[
            validators.DataRequired(),
            validators.Email()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    password = forms.PasswordField(
        "Пароль",
        validators=[
            validators.DataRequired(),
            validators.Length(min=8)
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    confirm_password = forms.PasswordField(
        "Подтверждение пароля",
        validators = [
            validators.DataRequired(),
            validators.EqualTo("password")
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    submit = forms.SubmitField(
        label = "Зарегистрироваться",
        render_kw = {
            "class": "btn btn-sm btn-primary"
        }
    )

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise forms.ValidationError("Это имя уже занято.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
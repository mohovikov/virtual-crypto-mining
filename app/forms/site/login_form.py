from flask_wtf import FlaskForm
import wtforms as forms
import wtforms.validators as validators


class LoginForm(FlaskForm):
    username = forms.StringField(
        label = "Имя пользователя",
        validators = [
            validators.DataRequired()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    password = forms.PasswordField(
        label = "Пароль",
        validators = [
            validators.DataRequired()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    remember = forms.BooleanField(
        label = "Запомнить меня",
        render_kw = {
            "class": "form-check-input"
        }
    )
    submit = forms.SubmitField(
        label = "Войти",
        render_kw = {
            "class": "btn btn-sm btn-primary"
        }
    )
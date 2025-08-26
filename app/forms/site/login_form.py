from flask_wtf import FlaskForm
import wtforms as forms
import wtforms.validators as validators


class LoginForm(FlaskForm):
    username = forms.StringField(
        "Имя пользователя",
        validators=[validators.DataRequired()]
    )
    password = forms.PasswordField(
        "Пароль",
        validators=[validators.DataRequired()]
    )
    remember = forms.BooleanField("Запомнить меня")
    submit = forms.SubmitField("Войти")
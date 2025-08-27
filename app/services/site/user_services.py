from typing import Optional
from app.extensions import db
from app.forms.site import RegisterForm, LoginForm
from app.models import User


def register_user(form: RegisterForm):
    user = User(
        username = str(form.username.data),
        email = str(form.email.data)
    )
    user.set_password(str(form.confirm_password.data))

    try:
        db.session.add(user)
        db.session.commit()

        return True, "Аккаунт успешно создан, теперь вы можете войти!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при регистрации:<br>{ex}", "danger"

def login_user(form: LoginForm):
    user: Optional[User] = User.query.filter_by(username = form.username.data).first()

    if user is not None and user.check_password(str(form.password.data)):
        return user, f"С возвращением, {user.username}", "success"

    return None, "Неверные имя пользователя и пароль.", "danger"
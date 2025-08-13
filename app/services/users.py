from typing import Optional
from app.extensions import db, bcrypt
from app.forms.site_forms import LoginForm, RegisterForm
from app.models.users import Users


def create_user(form: RegisterForm) -> tuple[bool, str, str]:
    hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = Users(
        username=str(form.username.data),
        email=str(form.email.data),
        password_hash=hashed_pw
    )

    try:
        db.session.add(user)
        db.session.commit()
        return True, "Аккаунт успешно создан! Теперь вы можете войти.", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при регистрации пользователя: {ex}", "danger"

def login_user(form: LoginForm):
    user: Optional[Users] = Users.query.filter_by(username=form.username.data).first()
    if user is not None and bcrypt.check_password_hash(user.password_hash, form.password.data):
        return user, f"С возвращением, {user.username}", "success"

    return None, "Неверные имя пользователя и пароль.", "danger"

def get_all_users(page: int):
    return Users.query.order_by(Users.id.asc()).paginate(
        page=page, per_page=50, error_out=False
    )

def get_user_data(id):
    return Users.query.get(id)
import os
from sqlalchemy import func, text

from app.config import Config
from app.extensions import db
from app.helpers import images_helper as image
from app.constants.privileges import Privileges
from app.forms.admin import SettingsForm
from app.models import User


def get_user_stats() -> dict[str, str]:
    results: dict = {}
    queries = {
        "total_users": "SELECT COUNT(*) FROM users",
        "banned_users": "SELECT COUNT(*) FROM users WHERE (privileges & 1 = 0 OR privileges = 1)",
        "mod_users": "SELECT COUNT(*) FROM users WHERE privileges & :admin_rap > 0",
        "sponsors": "SELECT COUNT(*) FROM users WHERE privileges & :user_sponsor > 0",
    }

    # total_users
    results['total_users'] = db.session.execute(
        text(queries['total_users'])
    ).scalar()

    # banned_users
    results['banned_users'] = db.session.execute(
        text(queries['banned_users'])
    ).scalar()
    
    # mod_users
    results['mod_users'] = db.session.execute(
        text(queries['mod_users']),
        {"admin_rap": Privileges.ADMIN_ACCESS_PANEL.value}
    ).scalar()
    
    # sponsors
    results['sponsors'] = db.session.execute(
        text(queries['sponsors']),
        {"user_sponsor": Privileges.USER_SPONSOR.value}
    ).scalar()

    return results

def get_all_users() -> list[User]:
    return User.query.all()

def get_user_by_id(user_id: int) -> User | None:
    return User.query.get(user_id)

def save_user_settings(user: User, form: SettingsForm):
    if not form.email.data or not form.privileges_value.data:
        raise Exception("Не все поля заполенны!")

    user.email = form.email.data
    user.country = form.country.data
    user.username_aka = form.username_aka.data
    user.userpage = form.userpage.data
    user.privileges = form.privileges_value.data

    try:
        db.session.commit()
        return "Настройки профиля были успешно сохранены!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при сохранении:<br>{ex}", "danger"

def user_manage_ban(user_id: int, action: str):
    user = get_user_by_id(user_id)
    if not user_id or not user:
        return "Хм… хотели поиграть с блокчейном, но майнер анонимный — мы не знаем, кого забанить или разблокировать!", "info"

    try:
        if action == "ban":
            user.privileges = user.privileges & ~Privileges.USER_NORMAL & ~Privileges.USER_ACTIVE
            db.session.commit()
            return f"Пользователь «{user.username}» был успешно забанен", "success"
        elif action == "unban":
            user.privileges = user.privileges | Privileges.USER_NORMAL | Privileges.USER_ACTIVE
            db.session.commit()
            return f"Пользователь «{user.username}» был успешно разбанен", "success"
        else:
            raise Exception(f"Хм… наш блокчейн не понимает, что за действие {action} вы указали. Майнеры в замешательстве!")

    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при выполнении задачи:<br>{ex}", "danger"

def user_manage_restrict(user_id: int, action: str):
    user = get_user_by_id(user_id)
    if not user_id or not user:
        return "Пользователь не найден!", "info"

    try:
        if action == "restrict":
            user.privileges = user.privileges & ~Privileges.USER_ACTIVE
            db.session.commit()
            return f"На пользователя «{user.username}» былы успешно наложены ограничения", "success"
        elif action == "unrestrict":
            user.privileges = user.privileges | Privileges.USER_ACTIVE
            db.session.commit()
            return f"С пользователя «{user.username}» успешно сняты ограничения", "success"
        else:
            raise Exception(f"Хм… наш блокчейн не понимает, что за действие {action} вы указали. Майнеры в замешательстве!")

    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при выполнении задачи:<br>{ex}", "danger"

def user_manage_image(user_id: int, action: str) -> tuple[bool, str, str]:
    user = get_user_by_id(user_id)
    if not user_id or not user:
        return False, "Пользователь не найден!", "info"

    try:
        if action == "delete_avatar":
            if not user.avatar_file:
                return False, f"У пользователя нет аватарки", "danger"

            user.avatar_file = None
            image.delete_user_image_folder(os.path.join(Config.USER_AVATAR_FOLDER, str(user.id)))
            db.session.commit()
            return True, "Аватарка пользователя была успешно удалена!", "success"
        elif action == "delete_background":
            if not user.background_file:
                return False, f"У пользователя нет фона профиля", "danger"

            user.background_file = None
            image.delete_user_image_folder(os.path.join(Config.USER_BACKGROUND_FOLDER, str(user.id)))
            db.session.commit()
            return True, "Фон профиля пользователя был успешно удален!", "success"
        else:
            raise Exception(f"Хм… наш блокчейн не понимает, что за действие {action} вы указали. Майнеры в замешательстве!")
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при выполнении задачи:<br>{ex}", "danger"
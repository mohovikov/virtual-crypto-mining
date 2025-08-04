from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from typing import Any
from flask import flash
from sqlalchemy import func

from blueprints.admin.forms import UserEditForm
from core import db
from core.constansts.privileges import Privileges
from core.models import Users

def get_all_users():
    return Users.query.all()

def get_users_stats() -> dict[str, Any]:
    total_users = db.session.query(func.count(Users.id)).scalar()
    sponsor_count = db.session.query(func.count(Users.id)).filter(
        Users.privileges.op('&')(Privileges.USER_SPONSOR) > 0
    ).scalar()
    restricted_count = db.session.query(func.count(Users.id)).filter(
        Users.privileges.op('&')(Privileges.USER_PUBLIC) == 0
    ).scalar()
    admin_count = db.session.query(func.count(Users.id)).filter(
        Users.privileges.op('&')(Privileges.ADMIN_ACCESS_PANEL) > 0
    ).scalar()

    return {
        "total_users": total_users,
        "sponsor_count": sponsor_count,
        "restricted_count": restricted_count,
        "admin_count": admin_count
    }

def get_user_by_id(id):
    user = Users.query.get(id)
    if not user:
        return False, "Пользователь не найден.", "warning"
    return True, user

def update_user(user: Users, form: UserEditForm) -> tuple[str, str]:
    try:
        user.username = str(form.username.data)
        user.username_aka = str(form.username_aka.data)
        user.userpage = str(form.userpage.data)
        user.email = str(form.email.data)
        user.privileges = int(str(form.privileges.data))
        user.country = str(form.country.data)

        db.session.commit()
        return f"Пользователь {user.username} успешно обновлён.", "success"
    except Exception as e:
        db.session.rollback()
        print(e)
        return f"Ошибка: {e}", "danger"


def give_sponsor(user: Users, duration: int, unit: str):
    try:
        now = datetime.now(timezone.utc)

        if unit == 'hours':
            delta = timedelta(hours=duration)
        elif unit == 'days':
            delta = timedelta(days=duration)
        elif unit == 'months':
            delta = relativedelta(months=duration)
        elif unit == 'years':
            delta = relativedelta(years=duration)

        expire_at = now + delta # type: ignore
        max_expire = now + relativedelta(years=1)

        if expire_at > max_expire:
            return False, "Максимальный срок — 1 год", "danger"

        user.sponsor_expire = expire_at
        user.privileges |= Privileges.USER_SPONSOR
        db.session.commit()
        return True, f"Спонсор выдан пользователю {user.username}", "success"
    except Exception as ex:
        print(ex)
        return False, f"Ошибка при выдачи спонсорства: {ex}", "danger"


def remove_sponsor(user: Users):
    try:
        user.privileges &= ~Privileges.USER_SPONSOR
        user.sponsor_expire = None
        db.session.commit()
        return True, f"Спонсорство снято с пользователя {user.username}", "warning"
    except Exception as ex:
        print(ex)
        return False, f"Ошибка при снятии спонсорства: {ex}", "danger"


def ban_user(id: int):
    user = Users.query.get(id)

    if not user:
        return "Пользователь не найден!", "warning"

    user.privileges = (user.privileges & ~Privileges.USER_NORMAL) & ~Privileges.USER_PUBLIC
    db.session.commit()
    # utils.add_logs(f"забанил пользователя {user.username}")
    return f"{user.username} забанен", "warning"


def unban_user(id: int):
    user = Users.query.get(id)

    if not user:
        return "Пользователь не найден!", "warning"

    user.privileges |= Privileges.USER_NORMAL
    user.privileges |= Privileges.USER_PUBLIC
    db.session.commit()
    # utils.add_logs(f"разбанил пользователя {user.username}")
    return f"{user.username} разбанен", "success"


def restrict_user(id: int):
    user = Users.query.get(id)

    if not user:
        return "Пользователь не найден!", "warning"

    user.privileges = (user.privileges | Privileges.USER_NORMAL) & ~Privileges.USER_PUBLIC
    db.session.commit()
    # utils.add_logs(f"ограничил {user.username}")
    return f"{user.username} ограничен", "warning"


def unrestrict_user(id: int):
    user = Users.query.get(id)

    if not user:
        return "Пользователь не найден!", "warning"

    user.privileges |= Privileges.USER_NORMAL
    user.privileges |= Privileges.USER_PUBLIC
    db.session.commit()
    # utils.add_logs(f"снял ограничения с {user.username}")
    return f"{user.username} разблокирован", "success"
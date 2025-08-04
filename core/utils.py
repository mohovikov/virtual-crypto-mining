from flask_login import current_user

from core.constansts.privileges import Privileges


def has_privilege(required_priv: Privileges, current_priv: int = -1) -> bool:
    if current_priv == -1:
        if not current_user.is_authenticated:
            return False
        current_priv = current_user.privileges

    return (current_priv & required_priv) > 0


def is_restricted(privileges: int) -> bool:
    return (
        not has_privilege(
            current_priv=privileges,
            required_priv=Privileges.USER_PUBLIC)
        and has_privilege(
            current_priv=privileges,
            required_priv=Privileges.USER_NORMAL
        )
    )


def is_banned(privileges) -> bool:
    return (
        not has_privilege(
            current_priv=privileges,
            required_priv=Privileges.USER_PUBLIC
        )
        and not has_privilege(
            current_priv=privileges,
            required_priv=Privileges.USER_NORMAL
        )
    )


def is_locked(privileges) -> bool:
    return (
        has_privilege(
            current_priv=privileges,
            required_priv=Privileges.USER_PUBLIC
        ) and not has_privilege(
            current_priv=privileges,
            required_priv=Privileges.USER_NORMAL
        )
    )

def check_user_status(privileges) -> dict[str, str]:
    if is_banned(privileges):
        return {
            "text": "Забанен",
            "color_class": "danger"
        }
    elif is_restricted(privileges):
        return {
            "text": "Ограничен",
            "color_class": "warning"
        }
    elif is_locked(privileges):
        return {
            "text": "Заблокирован",
            "color_class": "dark"
        }
    else:
        return {
            "text": "Ок",
            "color_class": "success"
        }

def get_privileges_checklist(user_privileges: int) -> list[dict]:
    result = []
    for name, privilege in Privileges.__members__.items():
        value = privilege.value
        if value <= 0:
            continue

        result.append({
            "name": name,
            "value": value,
            "checked": (user_privileges & value) > 0,
            "disabled": (value <= 2)
        })
    return result
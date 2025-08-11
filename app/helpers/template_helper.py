from app.models.privileges_groups import PrivilegesGroups
from app import privileges as priv


def check_user_status(privileges: int) -> tuple[str, str]:
    if priv.is_locked(privileges):
        return "Заблокирован", "dark"
    elif priv.is_banned(privileges):
        return "Забанен", "danger"
    elif priv.is_restricted(privileges):
        return "Ограничен", "warning"
    else:
        return "OK!", "success"

def get_privileges(user_privileges: int) -> list[dict]:
    result = []
    for name, privilege in priv.Privileges.__members__.items():
        if privilege.value <= 0:
            continue
        result.append({
            "name": name,
            "value": privilege.value,
            "checked": (user_privileges & privilege.value) > 0,
            "disabled": (privilege.value <= 2)
        })
    return result

def get_privilege_group(privileges: int):
    """Возвращает кортеж (name, color_class) для привилегии, или None если не найдено."""
    group = PrivilegesGroups.query.filter_by(privileges=privileges).first()
    if group:
        return {
            "name": group.name,
            "color_class": group.color_class
        }
    return None
from flask import request
from app.constants import Privileges


def check_user_status(privileges: int) -> tuple[str, str]:
    if Privileges.is_locked(privileges):
        return "Заблокирован", "dark"
    elif Privileges.is_banned(privileges):
        return "Забанен", "danger"
    elif Privileges.is_restricted(privileges):
        return "Ограничен", "warning"
    else:
        return "OK!", "success"

def get_privileges(user_privileges: int) -> list[dict]:
    result = []
    for name, privilege in Privileges.__members__.items():
        if privilege.value <= 0:
            continue
        result.append({
            "name": name,
            "value": privilege.value,
            "checked": (user_privileges & privilege.value) > 0,
            "disabled": (privilege.value <= 2)
        })
    return result

def is_active(endpoint):
    return 'active' if request.endpoint == endpoint else ''

def get_version():
    try:
        with open("version", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "unknown"
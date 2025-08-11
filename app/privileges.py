from enum import IntEnum, unique
from flask_login import current_user


@unique
class Privileges(IntEnum):
    USER_PUBLIC = 1 << 0
    USER_NORMAL = 2 << 0
    USER_SPONSOR = 2 << 1
    ADMIN_ACCESS_PANEL = 2 << 2
    ADMIN_MANAGE_USERS = 2 << 3

def has_privilege(privileges: Privileges, user_privileges: int = -1) -> bool:
    if user_privileges == -1:
        if current_user.is_anonymous:
            return False
        user_privileges = current_user.privileges

    return privileges & user_privileges != 0

def is_banned(privileges: int = -1) -> bool:
    """Бан: нет PUBLIC и нет NORMAL."""
    return (
        not has_privilege(Privileges.USER_PUBLIC, privileges)
        and not has_privilege(Privileges.USER_NORMAL, privileges)
    )

def is_restricted(privileges: int = -1) -> bool:
    """Ограничен: нет PUBLIC, но есть NORMAL."""
    return (
        not has_privilege(Privileges.USER_PUBLIC, privileges)
        and has_privilege(Privileges.USER_NORMAL, privileges)
    )

def is_locked(privileges: int = -1) -> bool:
    """Блокировка: есть PUBLIC, но нет NORMAL."""
    return (
        has_privilege(Privileges.USER_PUBLIC, privileges)
        and not has_privilege(Privileges.USER_NORMAL, privileges)
    )
from enum import IntEnum, unique
from flask_login import current_user


@unique
class Privileges(IntEnum):
    USER_PUBLIC             = 1 << 0
    USER_NORMAL             = 2 << 0
    USER_SPONSOR            = 2 << 1
    ADMIN_ACCESS_PANEL      = 2 << 2

    ADMIN_EDIT_USERS        = 2 << 3
    ADMIN_RESTRICT_USERS    = 2 << 4
    ADMIN_BAN_USERS         = 2 << 5
    ADMIN_LOCK_USERS        = 2 << 6

def has_privilege(privileges: Privileges, user_privileges: int = -1) -> bool:
    if user_privileges == -1:
        if current_user.is_anonymous:
            return False
        user_privileges = current_user.privileges

    return privileges & user_privileges != 0

def has_any_privilege(privileges_list: list[Privileges], user_privileges: int = -1) -> bool:
    for priv in privileges_list:
        if has_privilege(priv, user_privileges):
            return True
    return False

def is_locked(privileges: int = -1) -> bool:
    """Заблокирован: нет PUBLIC и нет NORMAL."""
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

def is_banned(privileges: int = -1) -> bool:
    """Ограничен: есть PUBLIC, но нет NORMAL."""
    return (
        has_privilege(Privileges.USER_PUBLIC, privileges)
        and not has_privilege(Privileges.USER_NORMAL, privileges)
    )
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

    ADMIN_MANAGE_PRIVILEGES = 2 << 7

    @classmethod
    def has_privilege(cls, privileges, user_privileges: int = -1) -> bool:
        if user_privileges == -1:
            if current_user.is_anonymous:
                return False
            user_privileges = current_user.privileges

        return (privileges & user_privileges) > 0

    @classmethod
    def has_any_privilege(cls, privileges_list, user_privileges: int = -1) -> bool:
        for priv in privileges_list:
            if cls.has_privilege(priv, user_privileges):
                return True
        return False

    @classmethod
    def is_locked(cls, privileges: int = -1) -> bool:
        """Заблокирован: нет PUBLIC и нет NORMAL."""
        return (
            not cls.has_privilege(Privileges.USER_PUBLIC, privileges)
            and not cls.has_privilege(Privileges.USER_NORMAL, privileges)
        )

    @classmethod
    def is_restricted(cls, privileges: int = -1) -> bool:
        """Ограничен: нет PUBLIC, но есть NORMAL."""
        return (
            not cls.has_privilege(Privileges.USER_PUBLIC, privileges)
            and cls.has_privilege(Privileges.USER_NORMAL, privileges)
        )

    @classmethod
    def is_banned(cls, privileges: int = -1) -> bool:
        """Ограничен: есть PUBLIC, но нет NORMAL."""
        return (
            cls.has_privilege(Privileges.USER_PUBLIC, privileges)
            and not cls.has_privilege(Privileges.USER_NORMAL, privileges)
        )
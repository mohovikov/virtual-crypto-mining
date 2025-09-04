from enum import IntEnum, unique
from flask_login import current_user


@unique
class Privileges(IntEnum):
    USER_ACTIVE = 1 << 0
    USER_NORMAL = 2 << 0
    USER_SPONSOR = 2 << 1
    ADMIN_ACCESS_PANEL = 2 << 2

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
    def is_banned(cls, privileges: int = -1) -> bool:
        """Заблокирован: нет USER_ACTIVE и нет USER_NORMAL."""
        return (
            not cls.has_privilege(Privileges.USER_ACTIVE, privileges)
            and not cls.has_privilege(Privileges.USER_NORMAL, privileges)
        )

    @classmethod
    def is_restricted(cls, privileges: int = -1) -> bool:
        """Ограничен: нет USER_ACTIVE, но есть USER_NORMAL."""
        return (
            not cls.has_privilege(Privileges.USER_ACTIVE, privileges)
            and cls.has_privilege(Privileges.USER_NORMAL, privileges)
        )

    @classmethod
    def check_account_status(cls, privileges: int = -1):
        if cls.is_banned(privileges):
            return "Аккаунт забанен", "danger"
        elif cls.is_restricted(privileges):
            return "Аккаунт ограничен", "warning"

        return "Аккаунт активен", "success"
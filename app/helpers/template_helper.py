from app import p


def check_user_status(privileges: int) -> tuple[str, str]:
    if p.is_locked(privileges):
        return "Заблокирован", "dark"
    elif p.is_banned(privileges):
        return "Забанен", "danger"
    elif p.is_restricted(privileges):
        return "Ограничен", "warning"
    else:
        return "Ok!", "success"
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

from app.extensions import db
from app.constants import Privileges
from app.models import User, UserBadge
from app.forms.admin import SponsorAwardForm


def give_sponsorship(user: User, form: SponsorAwardForm) -> tuple[bool, str, str]:
    now = datetime.now(timezone.utc)

    if not form.amount.data:
        raise Exception("Не указан срок выдачи")

    try:
        current = user.sponsor_expire
        if current and current.tzinfo is None:
            current = current.replace(tzinfo = timezone.utc)
        elif current:
            current = current.astimezone(timezone.utc)

        base_date = current if (current and current > now) else now

        if form.type.data == "add":
            new_expire = base_date + relativedelta(months = form.amount.data)
        elif form.type.data == "remove":
            new_expire = base_date - relativedelta(months = form.amount.data)
        else:
            raise ValueError("Неверный тип операции (ожидается 'add' или 'remove')")

        badge = UserBadge.query.filter_by(user_id = user.id, badge_id = 1).first()

        if new_expire <= now:
            if badge:
                db.session.delete(badge)
            user.sponsor_expire = None
            user.privileges &= ~Privileges.USER_SPONSOR
            db.session.commit()
            return True, f"Спонсорство для {user.username} снято", "warning"

        user.sponsor_expire = new_expire
        user.privileges |= Privileges.USER_SPONSOR
        if not badge:
            user_badge = UserBadge(user_id = user.id, badge_id = 1)
            db.session.add(user_badge)
        db.session.commit()

        action_text = "Продлено" if form.type.data == "add" else "Сокращено"

        return True, f"Статус спонсор для пользователя {user.username} изменен!<br>{action_text} на {form.amount.data} мес.", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при выдаче спонсорства:<br>{ex}", "danger"
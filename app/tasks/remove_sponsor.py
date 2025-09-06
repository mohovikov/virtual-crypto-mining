from datetime import datetime, timezone
from flask import Flask

from app.extensions import db
from app.constants import Privileges
from app.models import User, UserBadge


def remove_users_sponsorships_expired(app: Flask):
    with app.app_context():
        now = datetime.now(timezone.utc)
        expired_users: list[User] = User.query.filter(User.sponsor_expire <= now).all()
        count = 0

        for user in expired_users:
            badge = UserBadge.query.filter_by(user_id = user.id, badge_id = 1).first()
            if badge:
                db.session.delete(badge)
            user.sponsor_expire = None
            user.privileges &= ~Privileges.USER_SPONSOR
            db.session.add(user)
            count += 1

        db.session.commit()
        app.logger.info(f"[Tasks] Снято спонсорство у {count} пользователей")
from typing import Any, List

from flask_login import current_user
from core import db
from core.models import Logs


def get_all_logs() -> List[Any]:
    return Logs.query.all()

def get_logs_paginated(page: int = 1, per_page: int = 15):
    return Logs.query.order_by(Logs.created_at.desc()).paginate(page=page, per_page=per_page)

def add_log(text: str, uid: int = -1, through: str = "VCMAP") -> None:
    log = Logs(
        uid=current_user.id if uid == -1 else uid,
        text=text,
        through=through
    )
    try:
        db.session.add(log)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print(ex)
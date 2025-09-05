from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import BaseMixin


if TYPE_CHECKING:
    from app.models import User, Badge

class UserBadge(db.Model, BaseMixin):
    __tablename__ = "user_badges"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        autoincrement = True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete = "CASCADE"),
        nullable = False
    )
    badge_id: Mapped[int] = mapped_column(
        ForeignKey("badges.id", ondelete = "CASCADE"),
        nullable = False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="badges"
    )
    badge: Mapped["Badge"] = relationship(
        "Badge",
        back_populates="users"
    )

    def __init__(self, user_id: int, badge_id: int) -> None:
        self.user_id = user_id
        self.badge_id = badge_id
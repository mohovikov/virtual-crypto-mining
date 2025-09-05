from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import BaseMixin

if TYPE_CHECKING:
    from app.models import UserBadge

class Badge(db.Model, BaseMixin):
    __tablename__ = "badges"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        autoincrement = True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable = True
    )
    icon: Mapped[str] = mapped_column(
        String(64),
        nullable = False
    )
    color: Mapped[str] = mapped_column(
        String(64),
        nullable = False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc),
        server_default = text("UTC_TIMESTAMP()"),
        nullable = False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate = lambda: datetime.now(timezone.utc),
        server_default = text("UTC_TIMESTAMP()"),
        nullable = False
    )

    users: Mapped[list["UserBadge"]] = relationship(
        "UserBadge",
        back_populates="badge",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __init__(self, name: str, description: str | None, icon: str, color: str) -> None:
        self.name = name
        self.description = description
        self.icon = icon
        self.color = color
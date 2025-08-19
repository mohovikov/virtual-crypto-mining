from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from typing import Optional
import sqlalchemy as sa

from app.extensions import db
from app.models.base import InnoDBMixin


class PrivilegesGroup(db.Model, InnoDBMixin):
    __tablename__ = "privileges_groups"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(sa.String(30), nullable=False, unique=True, index=True)
    privileges: Mapped[Optional[int]] = mapped_column(sa.Integer, nullable=False)
    color_class: Mapped[Optional[str]] = mapped_column(sa.String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def __init__(self, name: str | None, privileges: int | None, color_class: str | None) -> None:
        self.name = name
        self.privileges = privileges
        self.color_class = color_class
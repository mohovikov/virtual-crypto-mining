from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class PrivilegesGroups(db.Model):
    __tablename__ = "privileges_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True, index=True)
    privileges: Mapped[int] = mapped_column(Integer, nullable=False)
    color_class: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(self, name: str, privileges: int, color_class: str | None) -> None:
        self.name = name
        self.privileges = privileges
        self.color_class = color_class
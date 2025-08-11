from datetime import datetime, timezone
from typing import Optional
from flask_login import UserMixin
from sqlalchemy import Integer, String, Text, DateTime, CHAR
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db, login_manager


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True, index=True)
    username_aka: Mapped[str] = mapped_column(String(32), nullable=True)
    userpage: Mapped[str] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    privileges: Mapped[int] = mapped_column(Integer, default=3)
    country: Mapped[str] = mapped_column(CHAR(2), default="XX")
    support_expire: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=None)
    register_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(self, username: str, email: str, password_hash: str) -> None:
        self.username = username
        self.email = email
        self.password_hash = password_hash


@login_manager.user_loader
def load_user(uid):
    return Users.query.get(uid)
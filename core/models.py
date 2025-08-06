from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from core import db, utils


class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    username_aka: Mapped[str] = mapped_column(String(50), nullable=True)
    userpage: Mapped[str] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(2), nullable=True)  # ISO-код страны

    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    privileges: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    sponsor_expire: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    @property
    def is_banned(self) -> bool:
        return utils.is_banned(self.privileges)

    @property
    def is_locked(self) -> bool:
        return utils.is_locked(self.privileges)

    @property
    def is_restricted(self) -> bool:
        return utils.is_restricted(self.privileges)

    def __init__(self, username: str, email: str, password_hash: str) -> None:
        self.username = username
        self.email = email
        self.password_hash = password_hash

class PrivilegesGroups(db.Model):
    __tablename__ = "privileges_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    privileges: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    color_class: Mapped[str] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, name: str, privileges: int, color_class: str) -> None:
        self.name = name
        self.privileges = privileges
        self.color_class = color_class

class Logs(db.Model):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    through: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Logs id={self.id} uid={self.uid} created_at={self.created_at}>"
    
    def __init__(self, uid:int, text: str, through: str) -> None:
        self.uid = uid
        self.text = text
        self.through = through
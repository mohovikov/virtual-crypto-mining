from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from core import db, utils

class CryptoCurrencies(db.Model):
    __tablename__ = "cryptocurrencies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cid: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(18, 2), nullable=True)
    icon_name: Mapped[Optional[str]] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Cryptocurrency id={self.id} cid={self.cid} name={self.name}>"

    def __init__(self, cid: int, name: str, symbol: str, price: float, icon_name: str | None) -> None:
        self.cid = cid
        self.name = name
        self.symbol = symbol
        self.price = price
        self.icon_name = icon_name or None

class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    username_aka: Mapped[str] = mapped_column(String(50), nullable=True)
    userpage: Mapped[str] = mapped_column(Text, nullable=True)
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

class UsersDeleted(db.Model):
    __tablename__ = "users_deleted"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reason: Mapped[str] = mapped_column(Text, nullable=True)

    def __init__(self, username: str, email: str, reason: str) -> None:
        self.username = username
        self.email = email
        self.reason = reason

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
    uid: Mapped[int] = mapped_column(ForeignKey("users.id", name="fk_logs_users_uid"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    through: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    user: Mapped["Users"] = relationship("Users", backref="logs")

    def __repr__(self):
        return f"<Logs id={self.id} uid={self.user.username} created_at={self.created_at}>"
    
    def __init__(self, uid:int, text: str, through: str) -> None:
        self.uid = uid
        self.text = text
        self.through = through
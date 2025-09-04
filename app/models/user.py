from datetime import datetime, timezone
from typing import Optional
from flask_login import UserMixin
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager
from app.models import BaseMixin


class User(db.Model, UserMixin, BaseMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        sa.String(32),
        nullable=False,
        unique=True,
        index=True
    )
    username_aka: Mapped[Optional[str]] = mapped_column(
        sa.String(32),
        nullable=True
    )
    email: Mapped[str] = mapped_column(
        sa.String(254),
        nullable=False,
        unique=True,
        index=True
    )
    password_hash: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False
    )
    userpage: Mapped[Optional[str]] = mapped_column(
        sa.Text,
        nullable=True
    )
    privileges: Mapped[int] = mapped_column(
        sa.BigInteger,
        default=3,
        nullable=False,
        index=True,
        server_default="3"
    )
    avatar_file: Mapped[Optional[str]] = mapped_column(
        sa.String(255),
        nullable=True
    )
    background_file: Mapped[Optional[str]] = mapped_column(
        sa.String(255),
        nullable=True
    )
    country: Mapped[str] = mapped_column(
        sa.CHAR(2),
        default="XX",
        server_default="XX",
        nullable=False
    )
    sponsor_expire: Mapped[Optional[datetime]] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=True
    )
    register_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=sa.text("UTC_TIMESTAMP()"),
        nullable=False
    )

    def __init__(self, username: str, email: str) -> None:
        self.username = username
        self.email = email

    def set_password(self, password: str):
        """Хэширует пароль и сохраняет в password_hash"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password: str) -> bool:
        """Проверяет пароль по хэшу"""
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
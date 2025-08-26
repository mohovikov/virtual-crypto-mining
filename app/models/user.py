from datetime import datetime, timezone
from typing import Optional
from flask_login import UserMixin
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

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
        sa.String(30),
        nullable=False,
        unique=True,
        index=True
    )
    username_aka: Mapped[str] = mapped_column(
        sa.String(32),
        nullable=True
    )
    email: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
        unique=True
    )
    password_hash: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False
    )
    userpage: Mapped[str] = mapped_column(
        sa.Text,
        nullable=True
    )
    privileges: Mapped[int] = mapped_column(
        sa.BigInteger,
        default=3
    )
    avatar_file: Mapped[Optional[str]] = mapped_column(
        sa.String(255),
        nullable=True
    )
    country: Mapped[str] = mapped_column(
        sa.CHAR(2),
        default="XX"
    )
    sponsor_expire: Mapped[Optional[datetime]] = mapped_column(
        sa.DateTime(timezone=True),
        default=None,
        nullable=True
    )
    register_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)
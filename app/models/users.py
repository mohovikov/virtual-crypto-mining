from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from app.extensions import db, login_manager


if TYPE_CHECKING:
    from app.models.clan_member import ClanMember

class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(sa.String(30), nullable=False, unique=True, index=True)
    username_aka: Mapped[str] = mapped_column(sa.String(32), nullable=True)
    userpage: Mapped[str] = mapped_column(sa.Text, nullable=True)
    email: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    privileges: Mapped[int] = mapped_column(sa.Integer, default=3)
    country: Mapped[str] = mapped_column(sa.CHAR(2), default="XX")
    sponsor_expire: Mapped[Optional[datetime]] = mapped_column(sa.DateTime(timezone=True), default=None)
    register_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    clans_joined: Mapped[list["ClanMember"]] = relationship("ClanMember", back_populates="user")

    def __init__(self, username: str, email: str, password_hash: str, sponsor_expire: datetime | None = None) -> None:
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.sponsor_expire = sponsor_expire


@login_manager.user_loader
def load_user(uid):
    return Users.query.get(uid)
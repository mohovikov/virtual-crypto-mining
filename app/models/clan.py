from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import List, Optional, TYPE_CHECKING
import sqlalchemy as sa

from app.extensions import db
from app.models.base import InnoDBMixin


if TYPE_CHECKING:
    from app.models.users import Users
    from app.models.clan_member import ClanMember

class Clan(db.Model, InnoDBMixin):
    __tablename__ = 'clans'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True)
    short_name: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True)
    logo_file: Mapped[Optional[str]] = mapped_column(sa.String(255), nullable=True)
    header_file: Mapped[Optional[str]] = mapped_column(sa.String(255), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(sa.String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(sa.Text, nullable=True)
    is_open: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=True)

    leader_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete='CASCADE'),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # отношения
    members: Mapped[List["ClanMember"]] = relationship(back_populates="clan")
    leader: Mapped["Users"] = relationship(back_populates="led_clans", foreign_keys=[leader_id])

    def __repr__(self):
        return f"<Clan {self.name}>"
    
    def __init__(
            self,
            name: str,
            short_name: str,
            is_open: bool,
            leader_id: int,
            logo_file: str | None = None,
            header_file: str | None = None,
            url: str | None = None,
            description: str | None = None
        ) -> None:
        self.name = name
        self.short_name = short_name
        self.is_open = is_open
        self.leader_id = leader_id

        self.logo_file = logo_file
        self.header_file = header_file
        self.url = url
        self.description = description

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import TYPE_CHECKING
import sqlalchemy as sa

from app.extensions import db
from app.models.base import InnoDBMixin


if TYPE_CHECKING:
    from app.models.users import Users
    from app.models.clan import Clan

class ClanMember(db.Model, InnoDBMixin):
    __tablename__ = "clan_members"

    user_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    clan_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("clans.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Связи
    clan: Mapped["Clan"] = relationship(back_populates="members")
    user: Mapped["Users"] = relationship(back_populates="clan_memberships")

    def __init__(self, user_id: int, clan_id: int) -> None:
        self.user_id = user_id
        self.clan_id = clan_id

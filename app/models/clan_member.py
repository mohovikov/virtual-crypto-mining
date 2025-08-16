from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
import sqlalchemy as sa

from app.constants import ClanPrivileges
from app.extensions import db


if TYPE_CHECKING:
    from app.models.users import Users
    from app.models.clan import Clan

class ClanMember(db.Model):
    __tablename__ = "clan_members"

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("users.id", ondelete="CASCADE", name="fk_clanm_user_id"),
        primary_key=True
    )
    clan_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("clans.id", ondelete="CASCADE", name="fk_clanm_clan_id"),
        nullable=False
    )

    privileges: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=False,
        default=ClanPrivileges.MEMBER
    )

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

    # Связи
    user: Mapped["Users"] = relationship("Users", back_populates="clans_joined")
    clan: Mapped["Clan"] = relationship("Clan", back_populates="members")

    __table_args__ = (
        sa.Index("ix_clanm_clan_id", "clan_id"),  # индекс для clan_id
    )

    def __init__(self, user_id: int, clan_id: int, privileges: int) -> None:
        self.user_id = user_id
        self.clan_id = clan_id
        self.privileges = privileges

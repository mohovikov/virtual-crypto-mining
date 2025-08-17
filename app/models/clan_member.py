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
        sa.ForeignKey("users.id", name="fk_clan_members_user_id_users"),
        primary_key=True,
    )
    clan_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("clans.id", name="fk_clan_members_clan_id_clans"),
        nullable=False,
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
    clan: Mapped["Clan"] = relationship(back_populates="members")
    user: Mapped["Users"] = relationship(back_populates="clan_memberships")

    __table_args__ = (
        sa.Index("ix_clan_members_clan_id", "clan_id"),
    )

    def __init__(self, user_id: int, clan_id: int) -> None:
        self.user_id = user_id
        self.clan_id = clan_id

from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import InnoDBMixin


if TYPE_CHECKING:
    from .users import User
    from .cryptocurrency import Cryptocurrency

class UserBalance(db.Model, InnoDBMixin):
    __tablename__ = "user_balances"

    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    crypto_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("cryptocurrencies.id", ondelete="CASCADE"), primary_key=True)
    balance: Mapped[float] = mapped_column(sa.Numeric(36, 18), nullable=False, default=0.000000000000000000)

    user: Mapped["User"] = relationship("User", back_populates="balances")
    crypto: Mapped["Cryptocurrency"] = relationship("Cryptocurrency", back_populates="balances")

    def __repr__(self):
        return f"<UserBalance user={self.user_id}, crypto={self.crypto_id}, balance={self.balance}>"
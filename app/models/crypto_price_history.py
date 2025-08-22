from datetime import datetime, timezone
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import InnoDBMixin

if TYPE_CHECKING:
    from .cryptocurrency import Cryptocurrency

class CryptoPriceHistory(db.Model, InnoDBMixin):
    __tablename__ = "crypto_price_history"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    crypto_id: Mapped[int] = mapped_column(sa.ForeignKey("cryptocurrencies.id"))
    price: Mapped[float] = mapped_column(sa.Numeric(36,2))
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    crypto: Mapped["Cryptocurrency"] = relationship("Cryptocurrency", back_populates="history")

    def __init__(self, crypto_id: int, price: float) -> None:
        self.crypto_id = crypto_id
        self.price = price
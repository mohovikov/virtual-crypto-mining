from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import InnoDBMixin


if TYPE_CHECKING:
    from .user_balance import UserBalance
    from .crypto_price_history import CryptoPriceHistory

class Cryptocurrency(db.Model, InnoDBMixin):
    __tablename__ = "cryptocurrencies"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    symbol: Mapped[str] = mapped_column(sa.String(20), unique=True, nullable=False)
    icon_file: Mapped[Optional[str]] = mapped_column(sa.String(255), nullable=True)
    price: Mapped[float] = mapped_column(sa.Numeric(36,2), nullable=False, default=0.00)
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

    balances: Mapped[List["UserBalance"]] = relationship("UserBalance", back_populates="crypto", cascade="all, delete-orphan")
    history: Mapped[list["CryptoPriceHistory"]] = relationship(
        "CryptoPriceHistory", back_populates="crypto", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Crypto {self.symbol}>"
    
    def __init__(self, name: str, symbol: str, price: float, logo_file: str | None = None) -> None:
        self.name = name
        self.symbol = symbol
        self.logo_file = logo_file
        self.price = price
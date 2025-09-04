from sqlalchemy import (
    Integer,
    BigInteger,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models import BaseMixin


class PrivilegesGroup(db.Model, BaseMixin):
    __tablename__ = "privileges_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    privileges: Mapped[int] = mapped_column(BigInteger, nullable=False)
    color: Mapped[str] = mapped_column(String(32), nullable=False)

    def __init__(self, name: str, privileges: int, color: str) -> None:
        self.name = name
        self.privileges = privileges
        self.color = color
from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class SchedulerLog(db.Model):
    __tablename__ = "scheduler_logs"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    job_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    message: Mapped[str] = mapped_column(sa.Text, nullable=True)
    is_success: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def __init__(self, job_name: str, message: str, is_success: bool = True) -> None:
        self.job_name = job_name
        self.message = message
        self.is_success = is_success
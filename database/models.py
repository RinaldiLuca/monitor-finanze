from database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_id: Mapped[str | None] = mapped_column(
        unique=True, index=True, nullable=True
    )

    operation_date: Mapped[date] = mapped_column(nullable=False)
    value_date: Mapped[date] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str | None] = mapped_column(nullable=True)
    account: Mapped[str | None] = mapped_column(nullable=True)

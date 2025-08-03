from database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    external_id: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    source_file_id: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    hash_key: Mapped[str] = mapped_column(nullable=False, index=True)

    booking_dt: Mapped[date] = mapped_column(nullable=False)
    value_dt: Mapped[date] = mapped_column(nullable=False, index=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str | None] = mapped_column(nullable=True)
    account: Mapped[str | None] = mapped_column(nullable=True)

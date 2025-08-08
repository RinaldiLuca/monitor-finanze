from datetime import date
from pydantic import BaseModel
from typing import Literal


class TransactionBase(BaseModel):
    external_id: str | None = None
    source_file_id: str | None = None
    hash_key: str

    booking_dt: date | None = None
    value_dt: date
    amount: float
    description: str | None = None
    category: str | None = None
    account: str | None = None
    source: Literal["api", "pdf"]


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 compat con SQLAlchemy

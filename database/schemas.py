from datetime import date
from pydantic import BaseModel


class TransactionBase(BaseModel):
    external_id: str | None = None
    operation_date: date
    value_date: date
    amount: float
    description: str
    category: str | None = None
    account: str | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 compat con SQLAlchemy

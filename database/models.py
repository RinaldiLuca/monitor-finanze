from sqlalchemy import Column, Integer, String, Float, Date
from database.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(
        String, unique=True, nullable=True, index=True
    )  # id esterno opzionale

    operation_date = Column(Date, nullable=False)
    value_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=True)
    account = Column(String, nullable=True)

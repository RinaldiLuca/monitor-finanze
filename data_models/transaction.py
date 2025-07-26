from pydantic import BaseModel
from datetime import date
from typing import Optional

class ApiTransactionRaw(BaseModel):
    
class Transaction(BaseModel):
    id_transaction: str
    transaction_dt: date
    value_dt: date
    amount: float
    description: str
    id_account: str
    id_source: str
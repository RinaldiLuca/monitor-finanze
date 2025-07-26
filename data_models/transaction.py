from pydantic import BaseModel
from datetime import date
from typing import Optional

class BaseTransaction(BaseModel):
    transaction_dt: date
    value_dt: date
    amount: float
    description: Optional[str]

class ApiTransactionRaw(BaseTransaction):
    external_id: str

class OcrTransactionRaw(BaseTransaction):
    source_file_id: str

class ConsolidatedTransaction(BaseTransaction):
    transaction_id: str
    account_id: str
    source_id: str
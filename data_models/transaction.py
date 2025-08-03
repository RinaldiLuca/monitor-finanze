from pydantic import BaseModel, field_validator
from datetime import date
from typing import Literal
import hashlib


class BaseTransaction(BaseModel):
    booking_dt: date
    value_dt: date
    amount: float
    description: str | None = None

    @field_validator("description")
    @classmethod
    def trim_description(cls, v):
        if v is not None:
            return v.strip()
        return v


class ApiTransactionRaw(BaseTransaction):
    external_id: str
    source: Literal["api"] = "api"


class OcrTransactionRaw(BaseTransaction):
    source_file_id: str | None = None  # filename+rownumber
    filename = str
    row = int
    source: Literal["pdf"] = "pdf"

    @field_validator("source_file_id", mode="before")
    @classmethod
    def generate_source_file_id(cls, v, info):
        values = info.data
        filename = values.get("filename")
        row = values.get("row")
        if filename is not None and row is not None:
            return f"{filename}__{row}"
        return v


class ConsolidatedTransaction(BaseTransaction):
    external_id: str | None = None
    source_file_id: str | None = None
    row: int | None = None
    source: Literal["api", "pdf"]
    hash_key: str | None = None

    @classmethod
    def from_raw(cls, raw_tx: BaseModel) -> "ConsolidatedTransaction":
        data = raw_tx.model_dump()
        relevant = f"{data['value_dt']}_{data['amount']}_{(data.get('description') or '').lower()}"
        data["hash_key"] = hashlib.sha256(relevant.encode()).hexdigest()
        return cls.model_validate(data)

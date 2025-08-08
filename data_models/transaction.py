from pydantic import BaseModel, field_validator, model_validator
from datetime import date, datetime
from typing import Literal
import hashlib


class BaseTransaction(BaseModel):
    booking_dt: date | None = None
    value_dt: date
    amount: float
    description: str | None = None
    category: str | None = None
    account: str | None = None
    hash_key: str | None = None

    @field_validator("description", mode="before")
    @classmethod
    def parse_string(cls, v):
        if v.strip() == "":
            return None
        else:
            return v

    @staticmethod
    def parse_float(v) -> float:
        if isinstance(v, str):
            if v == "":
                return 0
            elif "," in v:
                return float(v.replace(".", "").replace(",", "."))
            else:
                raise ValueError
        else:
            return v

    @field_validator("amount", mode="before")
    @classmethod
    def parse_amount(cls, v):
        return cls.parse_float(v)

    @field_validator("booking_dt", "value_dt", mode="before")
    @classmethod
    def parse_dates(cls, v):
        if isinstance(v, str):
            for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue
            raise ValueError(f"Data in formato non valido: {v}")
        return v

    @model_validator(mode="after")
    def set_hash_key(self):
        """Calcola l'hash solo dopo che tutti i campi sono stati trasformati."""
        if not self.hash_key:
            relevant = (
                f"{self.value_dt}_{self.amount}_{(self.description or '').lower()}"
            )
            self.hash_key = hashlib.sha256(relevant.encode()).hexdigest()
        return self


class ApiTransactionRaw(BaseTransaction):
    external_id: str
    source: Literal["api"] = "api"


class OcrTransactionRaw(BaseTransaction):
    source_file_id: str | None = None  # filename+rownumber
    filename: str
    page: int
    tab: int
    row: int
    negative_amount: float | None = None
    source: Literal["pdf"] = "pdf"

    @field_validator("negative_amount", mode="before")
    @classmethod
    def parse_negative_amount(cls, v):
        return cls.parse_float(v)

    def model_post_init(self, __context):
        if self.filename:  # and self.row is not None and self.row is not None:
            self.source_file_id = f"{self.filename}_{self.page}_{self.tab}_{self.row}"
        if (
            isinstance(self.amount, float)
            and isinstance(self.negative_amount, float)
            and self.negative_amount is not None
        ):  # just to silence pydantic
            self.amount -= self.negative_amount


# class ConsolidatedTransaction(BaseTransaction):
#     ## Valuta se spostre questa classe nello schema del database, per poi nel process utilizzare direttamente la classe dallo schema, valutare se utilizzare CreateTransaction
#     external_id: str | None = None
#     source_file_id: str | None = None
#     source: Literal["api", "pdf"]
#     hash_key: str | None = None

#     category: None = None
#     account: None = None

#     @classmethod
#     def from_raw(cls, raw_tx: BaseModel) -> "ConsolidatedTransaction":
#         data = (
#             raw_tx.model_dump()
#         )  # exclude={"filename", "tab", "row", "negative_amount"})
#         relevant = f"{data['value_dt']}_{data['amount']}_{(data.get('description') or '').lower()}"
#         data["hash_key"] = hashlib.sha256(relevant.encode()).hexdigest()
#         return cls.model_validate(data)

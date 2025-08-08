from database.models import Transaction

# from data_models.transaction import BaseTransaction
from database.schemas import TransactionCreate, TransactionRead


def should_update(existing: TransactionRead, incoming: TransactionCreate) -> bool:
    return any(
        [
            existing.amount != incoming.amount,
            existing.value_dt != incoming.value_dt,
            existing.booking_dt != incoming.booking_dt,
            (existing.description or "").strip().lower()
            != (incoming.description or "").strip().lower(),
            # (existing.account or '') != (incoming.account or '')
        ]
    )

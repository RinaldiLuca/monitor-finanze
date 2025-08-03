from database.models import Transaction
from data_models.transaction import ConsolidatedTransaction


def should_update(existing: Transaction, incoming: ConsolidatedTransaction) -> bool:
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

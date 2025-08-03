"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from database.models import Transaction
from database.schemas import TransactionCreate

async def get_by_external_id(db: AsyncSession, external_id: str):
    result = await db.execute(select(Transaction).where(Transaction.external_id == external_id))
    return result.scalars().first()

async def create_or_update_transaction(db: AsyncSession, data: TransactionCreate):
    existing = None
    if data.external_id:
        existing = await get_by_external_id(db, data.external_id)

    if existing:
        # Aggiorna campi (esempio semplice, potresti scegliere cosa aggiornare)
        existing.date = data.date
        existing.amount = data.amount
        existing.description = data.description
        existing.category = data.category
        existing.account = data.account
        await db.commit()
        await db.refresh(existing)
        return existing
    else:
        new_tx = Transaction(**data.model_dump())
        db.add(new_tx)
        await db.commit()
        await db.refresh(new_tx)
        return new_tx

        """

from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import Transaction

# from database.schemas import TransactionCreate
from data_models.transaction import ConsolidatedTransaction


async def create_transaction(db: AsyncSession, data: ConsolidatedTransaction):
    db_item = Transaction(**data.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def update_transaction(
    db: AsyncSession, transaction_id: int, updated_data: ConsolidatedTransaction
) -> int:
    update_fields = {
        field: value
        for field, value in updated_data.model_dump().items()
        if hasattr(Transaction, field)
    }

    stmt = (
        update(Transaction)
        .where(Transaction.id == transaction_id)
        .values(**update_fields)
    )

    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount  # numero di righe aggiornate


async def get_transactions(db: AsyncSession):
    result = await db.execute(select(Transaction))
    return result.scalars().all()


async def load_existing_transactions(
    db: AsyncSession, date_from: date, date_to: date
) -> list[Transaction]:  # dict[str, Transaction]:
    result = await db.execute(
        select(Transaction).where(
            Transaction.value_dt >= date_from, Transaction.value_dt <= date_to
        )
    )
    transactions = result.scalars().all()
    # Costruisci un dict hash_key -> Transaction per accesso rapido
    return [tx for tx in transactions]  # {tx.hash_key: tx for tx in transactions}

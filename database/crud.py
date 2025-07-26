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

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import Transaction
from database.schemas import TransactionCreate


async def create_transaction(db: AsyncSession, data: TransactionCreate):
    db_item = Transaction(**data.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_transactions(db: AsyncSession):
    result = await db.execute(select(Transaction))
    return result.scalars().all()

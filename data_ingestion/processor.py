from datetime import date, timedelta
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from database import crud
from database.models import Transaction
from database.schemas import TransactionCreate, TransactionRead
from data_ingestion.matcher import should_update
from data_models.transaction import (
    OcrTransactionRaw,
    ApiTransactionRaw,
    # ConsolidatedTransaction,
)


async def process_transactions(
    db: AsyncSession,
    raw_txs: Sequence[OcrTransactionRaw | ApiTransactionRaw],
    # date_from: date,
    # date_to: date,
):
    date_from = min([tx.value_dt for tx in raw_txs]) + timedelta(days=-15)
    date_to = max([tx.value_dt for tx in raw_txs]) + timedelta(days=15)
    existing_txs = await crud.load_existing_transactions(db, date_from, date_to)

    for raw in raw_txs:
        incoming = TransactionCreate.model_validate(raw.model_dump())

        if incoming.source == "api":
            await process_ApiTransaction(
                db=db, incoming=incoming, existing_txs=existing_txs
            )
        elif incoming.source == "pdf":
            await process_OcrTransaction(
                db=db, incoming=incoming, existing_txs=existing_txs
            )
        else:
            pass


async def process_ApiTransaction(
    db: AsyncSession, incoming: TransactionCreate, existing_txs: list[TransactionRead]
):
    # I get the first element is exist, None otherwise
    same_external_id = next(
        (tx for tx in existing_txs if tx.external_id == incoming.external_id), None
    )
    same_hash_pdfs = next(
        (
            tx
            for tx in existing_txs
            if (tx.hash_key == incoming.hash_key and tx.source == "pdf")
        ),
        None,
    )  # check the hash only whether the source is 'pdf'

    updated_id = None
    if same_external_id is not None:
        if should_update(same_external_id, incoming):
            await crud.update_transaction(db, same_external_id.id, incoming)
            updated_id = same_external_id.id
    elif same_hash_pdfs is not None:
        await crud.update_transaction(db, same_hash_pdfs.id, incoming)
        updated_id = same_hash_pdfs.id
    else:
        # Assegna la Macrocategoria
        await crud.create_transaction(db, incoming)

    to_remove = next((tx for tx in existing_txs if tx.id == updated_id), None)
    if to_remove is not None:
        existing_txs.remove(to_remove)


async def process_OcrTransaction(
    db: AsyncSession, incoming: TransactionCreate, existing_txs: list[TransactionRead]
):
    # I get the first element is exist, None otherwise
    same_sourcef_id = next(
        (tx for tx in existing_txs if tx.source_file_id == incoming.source_file_id),
        None,
    )
    same_hash = next(
        (tx for tx in existing_txs if tx.hash_key == incoming.hash_key), None
    )  # check the hash only whether the source is 'pdf'

    updated_id = None
    if same_sourcef_id is not None:
        if should_update(same_sourcef_id, incoming):
            await crud.update_transaction(db, same_sourcef_id.id, incoming)
            updated_id = same_sourcef_id.id
    elif same_hash is not None:
        if should_update(same_hash, incoming) and same_hash.source == "pdf":
            await crud.update_transaction(db, same_hash.id, incoming)
            updated_id = same_hash.id
    else:
        # Assegna la Macrocategoria
        await crud.create_transaction(db, incoming)

    to_remove = next((tx for tx in existing_txs if tx.id == updated_id), None)
    if to_remove is not None:
        existing_txs.remove(to_remove)

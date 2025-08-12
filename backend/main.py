from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.dependancies import get_db
from database.schemas import TransactionRead
from database.crud import load_existing_transactions

DBSession = Annotated[AsyncSession, Depends(get_db)]

app = FastAPI()


@app.get("/transactions", response_model=list[TransactionRead])
async def read_transactions(db: DBSession):
    return await load_existing_transactions(db)

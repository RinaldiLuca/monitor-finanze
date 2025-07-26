from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"

# Crea l'engine asincrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Factory per creare sessioni asincrone
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Base per i modelli ORM (tabelle)
Base = declarative_base()

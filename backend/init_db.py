# File: init_db.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import asyncio
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:admin123@db:5432/techrca")
Base = declarative_base()
# Set up async engine & session
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# ✅ Your models should already be imported before calling create_all
from main import FlowLog, RCAReport  # Import models after Base declaration

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database initialized")

# Optional standalone run (CLI)
if __name__ == "__main__":
    asyncio.run(init_db())

# init_db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import asyncio
import os
import traceback

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:admin123@db:5432/techrca")

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db(max_retries=10, delay=3):
    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Database initialized successfully.")
            return
        except Exception as e:
            print(f"❌ Error initializing the database (attempt {attempt + 1}/{max_retries}): {e}")
            traceback.print_exc()
            await asyncio.sleep(delay)
    raise RuntimeError("❌ Could not connect to the database after several retries.")

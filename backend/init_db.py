# init_db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from db_base import Base  # ✅ import Base from new location
from sqlalchemy import text
import asyncio
import os
import traceback
# Import your models here
from models.flow_log import FlowLog  # ✅ make sure this file contains your SQLAlchemy models
from models.rca_reports import RCAReports  # ✅ make sure this file contains your SQLAlchemy models

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:admin123@db:5432/techrca")

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

# ✅ Only test DB connection
async def test_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful.")
    except OperationalError as e:
        print(f"❌ OperationalError: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()

# Run the desired function when this script is executed directly
if __name__ == "__main__":
    asyncio.run(test_connection())
    # Uncomment below to also initialize tables:
    # asyncio.run(init_db())
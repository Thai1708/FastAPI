from sqlmodel import SQLModel, Session
import timescaledb
import time
from .config import DATABASE_URL, DB_TIMEZONE

engine = None

def get_engine():
    global engine
    if engine is None:
        engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)
    return engine

def init_db(retries: int = 5, delay: int = 5):
    for i in range(retries):
        try:
            print("Creating database...")
            SQLModel.metadata.create_all(get_engine())
            print("Creating hypertables...")
            timescaledb.metadata.create_all(get_engine())
            return
        except Exception as e:
            print(f"DB connection failed ({i+1}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("Database not available after retries")

def get_session():
    with Session(get_engine()) as session:
        yield session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@db:5432/app")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Database dependency to be used in FastAPI endpoints.
    Creates a new database session for each request and closes it when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
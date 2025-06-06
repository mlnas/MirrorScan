from app.db.session import engine
from app.models.scan import Base

def init_db() -> None:
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)

def drop_db() -> None:
    """Drop all tables"""
    Base.metadata.drop_all(bind=engine) 
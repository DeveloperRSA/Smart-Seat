from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, declarative_base

'''
Database configuration for Smart Seat Allocation Platform.

This file handles:
- SQLite database connection
- Session management
- ORM base class
- FastAPI database dependency
'''


SQLALCHEMY_DATABASE_URL = "sqlite:///./smart_seat.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()

def get_db():
    """
    Provides a database session per request and ensures proper cleanup.
    Used with FastAPI Depends().
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
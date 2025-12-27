import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()



engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False,  # Set to True for SQL query logging during development
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine 
)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
\
    db = SessionLocal()

    try: 
        yield db 
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
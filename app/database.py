"""
Database configuration for the KADORA habit tracking application.

This module configures the SQLite database, creates the SQLAlchemy
engine and session factory, and provides a dependency for accessing
the database safely.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Database connection URL for the local SQLite database.
DATABASE_URL = "sqlite:///./kadora.db"


# Create the SQLAlchemy engine used to communicate with the database.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Configure the database session factory.
# Each session manages database operations for a unit of work.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class inherited by all SQLAlchemy database models.
Base = declarative_base()


def get_db():
    """
    Provide a database session for application operations.

    The session is yielded to the caller and closed in the
    finally block, ensuring cleanup even if an error occurs.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        
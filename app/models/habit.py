from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from ..database import Base


class Habit(Base):
    """
    SQLAlchemy model representing a habit tracked in KADORA.

    Each habit has a name, optional description, periodicity,
    and creation timestamp.
    """

    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    periodicity = Column(String, nullable=False, server_default="daily")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

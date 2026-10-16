from sqlalchemy import Column, Integer, Date, ForeignKey, UniqueConstraint

from ..database import Base


class Completion(Base):
    """
    SQLAlchemy model representing a recorded habit completion.

    Each record links a habit to a completion date. The unique
    constraint prevents the same habit from being completed
    more than once on the same date.
    """

    __tablename__ = "completions"

    __table_args__ = (
        UniqueConstraint(
            "habit_id",
            "completion_date",
            name="uq_habit_completion_date"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    completion_date = Column(Date, nullable=False)
    
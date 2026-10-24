"""
Seed the KADORA database with predefined habits and sample completions.

Creates five habits and four weeks of deterministic completion data
for development, testing, and demonstration purposes.

The script avoids inserting duplicate seed data when habits already
exist in the database.
"""

from datetime import date, datetime, timedelta

from app.database import SessionLocal, init_db
from app.models.habit import Habit
from app.models.completion import Completion
 
def seed_database():
    """
    Populate an empty database with KADORA demonstration data.

    Create five predefined habits and their four-week completion
    patterns. Commit changes on success, roll back on failure,
    and always close the database session.
    """
    init_db()
    db = SessionLocal()

    try:
        # Avoid inserting duplicate demonstration data.
        existing_habits = db.query(Habit).count()

        if existing_habits > 0:
            print("Database already contains habits.")
            print("clear development data before running seed.")
            return

        today = date.today()
        start_date = today - timedelta(days=27)

        habits = [
            {
                "name": "Drink 2L Water",
                "description": "Drink at least 2 litres of water each day.",
                "periodicity": "daily",
            },
            {
                "name": "Read 15 Pages",
                "description": "Read at least 15 pages each day.",
                "periodicity": "daily",
            },
            {
                "name": "Practice Python",
                "description": "Practice Python programming each day.",
                "periodicity": "daily",
            },
            {
                "name": "Deep Clean Apartment",
                "description": "Deep clean the apartment once each week.",
                "periodicity": "weekly",
            },
            {
                "name": "Review Finances",
                "description": "Review personal finances once each week.",
                "periodicity": "weekly",
            },
        ]

        created_habits = {}

        # Create the predefined habits and assign their creation dates.
        for habit_data in habits:
            habit = Habit(
                name=habit_data["name"],
                description=habit_data["description"],
                periodicity=habit_data["periodicity"],
                created_at=datetime.combine(
                    start_date,
                    datetime.min.time()
                ),
            )

            db.add(habit)
            db.flush()

            created_habits[habit.name] = habit

        # Define repeatable completion patterns for the 28-day demonstration period.
        daily_patterns = {
            "Drink 2L Water": [
                1, 1, 1, 0, 1, 1, 0,
                1, 1, 0, 1, 1, 1, 1,
                1, 0, 1, 1, 1, 0, 1,
                1, 1, 1, 0, 1, 1, 1,
            ],
            "Read 15 Pages": [
                1, 1, 0, 1, 1, 0, 1,
                1, 0, 1, 1, 1, 0, 1,
                1, 1, 1, 0, 1, 1, 0,
                1, 1, 0, 1, 1, 1, 1,
            ],
            "Practice Python": [
                1, 0, 1, 1, 0, 1, 1,
                1, 1, 1, 0, 1, 0, 1,
                1, 1, 0, 1, 1, 1, 0,
                1, 0, 1, 1, 1, 1, 1,
            ],
        }

        weekly_patterns = {
            "Deep Clean Apartment": [1, 0, 1, 1],
            "Review Finances": [1, 1, 0, 1],
        }

        # Create completion records for daily habits based on their patterns.
        for habit_name, pattern in daily_patterns.items():
            habit = created_habits[habit_name]

            for day_offset, completed in enumerate(pattern):
                if completed:
                    completion = Completion(
                        habit_id=habit.id,
                        completion_date=start_date
                        + timedelta(days=day_offset),
                    )

                    db.add(completion)

        # Create completion records for weekly habits based on their patterns.
        for habit_name, pattern in weekly_patterns.items():
            habit = created_habits[habit_name]

            for week, completed in enumerate(pattern):
                if completed:
                    completion = Completion(
                        habit_id=habit.id,
                        completion_date=start_date
                        + timedelta(days=week * 7),
                    )

                    db.add(completion)

        db.commit()

        print("KADORA seed data created successfully.")
        print("5 predefined habits added.")
        print("4 weeks of completion data added.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
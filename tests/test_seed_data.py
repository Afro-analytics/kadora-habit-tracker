from datetime import date, timedelta

from app.database import SessionLocal
from app.models.habit import Habit
from app.models.completion import Completion


def test_seeded_habits_exist():
    db = SessionLocal()

    try:
        habits = db.query(Habit).all()

        assert len(habits) == 5

        daily_habits = [
            habit for habit in habits
            if habit.periodicity == "daily"
        ]

        weekly_habits = [
            habit for habit in habits
            if habit.periodicity == "weekly"
        ]

        assert len(daily_habits) == 3
        assert len(weekly_habits) == 2

    finally:
        db.close()


def test_seeded_completions_exist():
    db = SessionLocal()

    try:
        habits = db.query(Habit).all()

        assert len(habits) == 5

        for habit in habits:
            completions = (
                db.query(Completion)
                .filter(Completion.habit_id == habit.id)
                .all()
            )

            assert len(completions) > 0

    finally:
        db.close()


def test_daily_habits_have_four_weeks_of_data():
    db = SessionLocal()

    try:
        daily_habits = (
            db.query(Habit)
            .filter(Habit.periodicity == "daily")
            .all()
        )

        assert len(daily_habits) == 3

        for habit in daily_habits:
            completions = (
                db.query(Completion)
                .filter(Completion.habit_id == habit.id)
                .order_by(Completion.completion_date)
                .all()
            )

            dates = [completion.completion_date for completion in completions]

            assert len(dates) > 0
            assert dates[-1] - dates[0] >= timedelta(days=27)

    finally:
        db.close()


def test_weekly_habits_have_four_weeks_of_data():
    db = SessionLocal()

    try:
        weekly_habits = (
            db.query(Habit)
            .filter(Habit.periodicity == "weekly")
            .all()
        )

        assert len(weekly_habits) == 2

        for habit in weekly_habits:
            completions = (
                db.query(Completion)
                .filter(Completion.habit_id == habit.id)
                .order_by(Completion.completion_date)
                .all()
            )

            assert len(completions) == 3

    finally:
        db.close()

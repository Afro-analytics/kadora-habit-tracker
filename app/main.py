"""
FastAPI application for the KADORA habit tracking system.

Provides endpoints for habit management, completion tracking,
streak calculations, dashboards, and habit analytics.
"""

from datetime import date

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from .database import engine, Base, get_db
from .models.habit import Habit
from .models.completion import Completion
from .services.streak_service import calculate_current_streak
from .services.habit_service import build_habit_summary
from .services.analytics_service import (
    filter_habits_by_periodicity,
    find_longest_streak_across_habits,
)

class HabitCreate(BaseModel):
    """Define the data required to create or update a habit."""

    name: str
    description: str = ""

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="KADORA API",
    description="Backend API for the KADORA habit tracking system.",
    version="1.0.0"
)


@app.get("/")
def root():
    """Check whether the KADORA API is running."""
    return {
        "message": "Welcome to KADORA",
        "status": "API is running"
    }

@app.post("/habits")
def create_habit(habit: HabitCreate, db=Depends(get_db)):
    """Create a new habit and save it to the database."""
    new_habit = Habit(
        name=habit.name,
        description=habit.description
    )

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return {
        "id": new_habit.id,
        "name": new_habit.name,
        "description": new_habit.description
    }

@app.get("/habits")
def get_habits(db=Depends(get_db)):
    """Retrieve all habits stored in the database."""
    habits = db.query(Habit).all()

    return [
        {
            "id": habit.id,
            "name": habit.name,
            "description": habit.description
        }
        for habit in habits
    ]

@app.get("/habits/summary")
def get_habits_summary(db=Depends(get_db)):
    """Retrieve summary statistics for all habits."""

    habits = db.query(Habit).all()

    summaries = []

    for habit in habits:
        completions = (
            db.query(Completion)
            .filter(Completion.habit_id == habit.id)
            .all()
        )

        summaries.append(
            build_habit_summary(
                habit,
                completions
            )
        )

    return summaries

@app.get("/habits/periodicity/{periodicity}")
def get_habits_by_periodicity(
    periodicity: str,
    db=Depends(get_db)
):
    """Retrieve habits matching the requested periodicity."""
    habits = db.query(Habit).all()

    filtered_habits = filter_habits_by_periodicity(
        habits,
        periodicity
    )

    return [
        {
            "id": habit.id,
            "name": habit.name,
            "description": habit.description,
            "periodicity": habit.periodicity,
        }
        for habit in filtered_habits
    ]

@app.get("/analytics/longest-streak")
def get_longest_streak_across_habits(
    db=Depends(get_db)
):
    """Calculate the longest streak across all habits."""
    habits = db.query(Habit).all()
    completions = db.query(Completion).all()

    longest_streak = find_longest_streak_across_habits(
        habits,
        completions
    )

    return {
        "longest_streak": longest_streak
    }

@app.get("/habits/{habit_id}/today")
def get_today_status(habit_id: int, db=Depends(get_db)):
    """Check whether a habit was completed today."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()

    if habit is None:
        return {
            "message": "Habit not found",
            "habit_id": habit_id
        }

    today = date.today()

    completion = (
        db.query(Completion)
        .filter(
            Completion.habit_id == habit_id,
            Completion.completion_date == today
        )
        .first()
    )

    return {
        "habit_id": habit_id,
        "date": today,
        "completed": completion is not None
    }

@app.get("/habits/{habit_id}")
def get_habit(habit_id: int, db=Depends(get_db)):
    """Retrieve details for a specific habit."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()

    if habit is None:
        return {
            "message": "Habit not found",
            "habit_id": habit_id
        }

    return {
        "id": habit.id,
        "name": habit.name,
        "description": habit.description
    }

@app.put("/habits/{habit_id}")
def update_habit(
    habit_id: int,
    habit_data: HabitCreate,
    db=Depends(get_db)
):
    """Update the name and description of an existing habit."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()

    if habit is None:
        return {
            "message": "Habit not found",
            "habit_id": habit_id
        }

    habit.name = habit_data.name
    habit.description = habit_data.description

    db.commit()
    db.refresh(habit)

    return {
        "id": habit.id,
        "name": habit.name,
        "description": habit.description
    }

@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db=Depends(get_db)):
    """Delete a habit and its associated completion records."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()

    if habit is None:
        return {
            "message": "Habit not found",
            "habit_id": habit_id
        }

    db.query(Completion).filter(
        Completion.habit_id == habit_id
    ).delete()

    db.delete(habit)
    db.commit()

    return {
        "message": "Habit deleted successfully",
        "habit_id": habit_id
    }

@app.post("/habits/{habit_id}/complete")
def complete_habit(habit_id: int, db=Depends(get_db)):
    """Record a completion for a habit for the current date."""
    completion = Completion(
        habit_id=habit_id,
        completion_date=date.today()
    )

    db.add(completion)
    db.commit()
    db.refresh(completion)

    return {
        "id": completion.id,
        "habit_id": completion.habit_id,
        "completion_date": completion.completion_date
    }

@app.get("/habits/{habit_id}/completions")
def get_habit_completions(habit_id: int, db=Depends(get_db)):
    """Retrieve all completion records for a specific habit."""
    completions = (
        db.query(Completion)
        .filter(Completion.habit_id == habit_id)
        .order_by(Completion.completion_date.desc())
        .all()
    )

    return [
        {
            "id": completion.id,
            "habit_id": completion.habit_id,
            "completion_date": completion.completion_date
        }
        for completion in completions
    ]

@app.get("/habits/{habit_id}/streak")
def get_habit_streak(habit_id: int, db=Depends(get_db)):
    """Calculate the current streak for a specific habit."""
    completions = (
        db.query(Completion)
        .filter(Completion.habit_id == habit_id)
        .all()
    )

    completion_dates = [
        completion.completion_date
        for completion in completions
    ]

    streak = calculate_current_streak(completion_dates)

    return {
        "habit_id": habit_id,
        "current_streak": streak
    }

@app.delete("/habits/{habit_id}/complete")
def undo_completion(habit_id: int, db=Depends(get_db)):
    """Remove today's completion record for a specific habit."""
    today = date.today()

    completion = (
        db.query(Completion)
        .filter(
            Completion.habit_id == habit_id,
            Completion.completion_date == today
        )
        .first()
    )

    if completion is None:
        return {
            "message": "No completion found for today",
            "habit_id": habit_id
        }

    db.delete(completion)
    db.commit()

    return {
        "message": "Today's completion removed",
        "habit_id": habit_id
    }

@app.get("/habits/{habit_id}/dashboard")
def get_habit_dashboard(habit_id: int, db=Depends(get_db)):
    """Retrieve a dashboard summary for a specific habit."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()

    if habit is None:
        return {
            "message": "Habit not found",
            "habit_id": habit_id
        }

    completions = (
        db.query(Completion)
        .filter(Completion.habit_id == habit_id)
        .all()
    )

    return build_habit_summary(habit, completions)


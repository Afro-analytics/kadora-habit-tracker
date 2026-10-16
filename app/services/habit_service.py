from datetime import date

from app.models.habit import Habit
from app.models.completion import Completion
from app.services.streak_service import (
    calculate_current_streak,
    calculate_longest_streak,
)


def build_habit_summary(habit: Habit, completions: list[Completion]):
    """
    Build an analytical summary for a habit.

    The summary combines completion information, current and longest
    streaks, total completions, active days, and completion rate.

    Args:
        habit: The Habit object being analysed.
        completions: Completion records belonging to the habit.

    Returns:
        A dictionary containing the habit's tracking and performance data.
    """
    completion_dates = [
        completion.completion_date
        for completion in completions
    ]

    today = date.today()

    completed_today = today in completion_dates

    current_streak = calculate_current_streak(
        completion_dates
    )

    longest_streak = calculate_longest_streak(
        completion_dates
    )

    total_completions = len(completions)

    days_active = (
        today - habit.created_at.date()
    ).days + 1

    if days_active < 1:
        days_active = 1

    completion_rate = (
        total_completions / days_active
    ) * 100

    return {
        "id": habit.id,
        "name": habit.name,
        "description": habit.description,
        "completed_today": completed_today,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_completions": total_completions,
        "days_active": days_active,
        "completion_rate": round(
            completion_rate,
            2
        )
    }

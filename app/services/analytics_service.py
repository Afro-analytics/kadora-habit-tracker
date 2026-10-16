from app.models.habit import Habit
from app.models.completion import Completion
from app.services.streak_service import calculate_longest_streak


def filter_habits_by_periodicity(
    habits: list[Habit],
    periodicity: str
):
    """
    Filter habits according to their periodicity.

    Args:
        habits: A collection of Habit objects.
        periodicity: The required periodicity, such as daily or weekly.

    Returns:
        A list containing habits matching the requested periodicity.
    """
    return [
        habit
        for habit in habits
        if habit.periodicity == periodicity
    ]


def find_longest_streak_across_habits(
    habits: list[Habit],
    completions: list[Completion]
):
    """
    Find the longest completion streak among all supplied habits.

    Args:
        habits: A collection of Habit objects.
        completions: A collection of Completion objects.

    Returns:
        The longest streak in days across all habits.
    """
    longest_streak = 0

    for habit in habits:
        completion_dates = [
            completion.completion_date
            for completion in completions
            if completion.habit_id == habit.id
        ]

        habit_longest_streak = calculate_longest_streak(
            completion_dates
        )

        if habit_longest_streak > longest_streak:
            longest_streak = habit_longest_streak

    return longest_streak

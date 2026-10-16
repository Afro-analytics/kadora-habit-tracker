from datetime import date

from app.services.streak_service import (
    calculate_current_streak,
    calculate_longest_streak,
)


def test_longest_streak_with_consecutive_dates():
    dates = [
        date(2026, 9, 1),
        date(2026, 9, 2),
        date(2026, 9, 3),
        date(2026, 9, 7),
        date(2026, 9, 8),
    ]

    assert calculate_longest_streak(dates) == 3


def test_longest_streak_with_empty_list():
    assert calculate_longest_streak([]) == 0


def test_longest_streak_with_single_date():
    dates = [date(2026, 9, 10)]

    assert calculate_longest_streak(dates) == 1


def test_current_streak_with_empty_list():
    assert calculate_current_streak([]) == 0
    
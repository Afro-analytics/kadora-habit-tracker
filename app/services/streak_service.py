from datetime import date, timedelta


def calculate_current_streak(completion_dates):
    """
    Calculate the current consecutive completion streak.

    A streak is considered current when the most recent completion
    occurred today or yesterday.

    Args:
        completion_dates: A collection of completion dates.

    Returns:
        The number of consecutive completion days.
    """
    if not completion_dates:
        return 0

    dates = sorted(set(completion_dates), reverse=True)

    today = date.today()

    # A streak is current only if the habit was completed today
    # or yesterday.
    if dates[0] < today - timedelta(days=1):
        return 0

    streak = 1
    current_date = dates[0]

    for completion_date in dates[1:]:
        expected_date = current_date - timedelta(days=1)

        if completion_date == expected_date:
            streak += 1
            current_date = completion_date
        else:
            break

    return streak


def calculate_longest_streak(completion_dates):
    """
    Calculate the longest consecutive completion streak.

    Args:
        completion_dates: A collection of completion dates.

    Returns:
        The longest consecutive streak in days.
    """
    if not completion_dates:
        return 0

    dates = sorted(set(completion_dates))

    longest_streak = 1
    current_streak = 1

    for i in range(1, len(dates)):
        difference = (dates[i] - dates[i - 1]).days

        if difference == 1:
            current_streak += 1

            if current_streak > longest_streak:
                longest_streak = current_streak

        else:
            current_streak = 1

    return longest_streak

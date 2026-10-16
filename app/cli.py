"""
Command-line interface for the KADORA habit tracking application.

Allows users to create, view, complete, analyse, and delete habits,
as well as access habit streaks and analytics from the terminal.
"""

from datetime import date

from app.database import SessionLocal
from app.models.completion import Completion
from app.models.habit import Habit
from app.services.streak_service import calculate_current_streak
from app.services.analytics_service import (
    filter_habits_by_periodicity,
    find_longest_streak_across_habits,
)
from app.services.habit_service import build_habit_summary


def main():
    """
    Run the KADORA interactive command-line application.

    Display the main menu, process user selections, perform
    database operations, and close the database session on exit.
    """
    print("Welcome to KADORA")
    print("Habit Tracking System")

    db = SessionLocal()

    try:
        while True:
            print("\nKADORA MENU")
            print("1. List habits")
            print("2. View habit")
            print("3. Create habit")
            print("4. Complete habit")
            print("5. View completions")
            print("6. View streak")
            print("7. View analytics")
            print("8. Delete habit")
            print("9. Exit")

            choice = input("\nChoose an option: ")

            if choice == "1":
                habits = db.query(Habit).all()

                if not habits:
                    print("\nNo habits found.")
                else:
                    print("\nYOUR HABITS")
                    for habit in habits:
                        print(f"{habit.id}. {habit.name} ({habit.periodicity})")

            elif choice == "2":
                try:
                    habit_id = int(input("Enter habit ID: "))
                except ValueError:
                    print("Invalid habit ID.")
                    continue

                habit = (
                    db.query(Habit)
                    .filter(Habit.id == habit_id)
                    .first()
                )

                if habit is None:
                    print("Habit not found.")
                else:
                    print("\nHABIT DETAILS")
                    print(f"ID: {habit.id}")
                    print(f"Name: {habit.name}")
                    print(f"Description: {habit.description}")
                    print(f"Periodicity: {habit.periodicity}")
                    print(f"Created: {habit.created_at}")

            elif choice == "3":
                name = input("Enter habit name: ").strip()
                description = input("Enter habit description: ").strip()
                periodicity = input(
                    "Enter periodicity (daily/weekly): "
                ).strip().lower()

                if not name:
                    print("Habit name cannot be empty.")

                elif periodicity not in ("daily", "weekly"):
                    print("Periodicity must be daily or weekly.")

                else:
                    new_habit = Habit(
                        name=name,
                        description=description,
                        periodicity=periodicity,
                    )

                    db.add(new_habit)
                    db.commit()
                    db.refresh(new_habit)

                    print("\nHabit created successfully.")
                    print(f"ID: {new_habit.id}")
                    print(f"Name: {new_habit.name}")
                    print(f"Periodicity: {new_habit.periodicity}")

            elif choice == "4":
                try:
                    habit_id = int(input("Enter habit ID: "))
                except ValueError:
                    print("Invalid habit ID.")
                    continue

                habit = (
                    db.query(Habit)
                    .filter(Habit.id == habit_id)
                    .first()
                )

                if habit is None:
                    print("Habit not found.")
                else:
                    completion = Completion(
                        habit_id=habit_id,
                        completion_date=date.today(),
                    )

                    db.add(completion)
                    db.commit()
                    db.refresh(completion)

                    print("\nHabit completed successfully.")
                    print(f"Habit: {habit.name}")
                    print(f"Date: {completion.completion_date}")

            elif choice == "5":
                try:
                    habit_id = int(input("Enter habit ID: "))
                except ValueError:
                    print("Invalid habit ID.")
                    continue

                habit = (
                    db.query(Habit)
                    .filter(Habit.id == habit_id)
                    .first()
                )

                if habit is None:
                    print("Habit not found.")
                else:
                    completions = (
                        db.query(Completion)
                        .filter(Completion.habit_id == habit_id)
                        .order_by(Completion.completion_date.desc())
                        .all()
                    )

                    print(f"\nCOMPLETIONS FOR: {habit.name}")

                    if not completions:
                        print("No completions recorded.")
                    else:
                        for completion in completions:
                            print(completion.completion_date)

            elif choice == "6":
                try:
                    habit_id = int(input("Enter habit ID: "))
                except ValueError:
                    print("Invalid habit ID.")
                    continue

                habit = (
                    db.query(Habit)
                    .filter(Habit.id == habit_id)
                    .first()
                )

                if habit is None:
                    print("Habit not found.")
                else:
                    completions = (
                        db.query(Completion)
                        .filter(Completion.habit_id == habit_id)
                        .all()
                    )

                    completion_dates = [
                        completion.completion_date
                        for completion in completions
                    ]

                    current_streak = calculate_current_streak(completion_dates)

                    print(f"\nSTREAK FOR: {habit.name}")
                    print(f"Current streak: {current_streak} day(s)")

            elif choice == "7":
                while True:
                    print("\nANALYTICS")
                    print("1. View daily habits")
                    print("2. View weekly habits")
                    print("3. View longest streak across all habits")
                    print("4. View specific habit analysis")
                    print("5. Back to main menu")

                    analytics_choice = input("\nChoose an option: ")

                    if analytics_choice == "1":
                        habits = db.query(Habit).all()
                        daily_habits = filter_habits_by_periodicity(habits, "daily")
                        print("\nDAILY HABITS")
                        if not daily_habits:
                            print("No daily habits found.")
                        else:
                            for habit in daily_habits:
                                print(f"{habit.id}. {habit.name}")

                    elif analytics_choice == "2":
                        habits = db.query(Habit).all()
                        weekly_habits = filter_habits_by_periodicity(habits, "weekly")
                        print("\nWEEKLY HABITS")
                        if not weekly_habits:
                            print("No weekly habits found.")
                        else:
                            for habit in weekly_habits:
                                print(f"{habit.id}. {habit.name}")

                    elif analytics_choice == "3":
                        habits = db.query(Habit).all()
                        completions = db.query(Completion).all()
                        longest_streak = find_longest_streak_across_habits(habits, completions)
                        print("\nLONGEST STREAK ACROSS ALL HABITS")
                        print(f"Longest streak: {longest_streak} day(s)")

                    elif analytics_choice == "4":
                        try:
                            habit_id = int(input("Enter habit ID: "))
                        except ValueError:
                            print("Invalid habit ID.")
                            continue

                        habit = db.query(Habit).filter(Habit.id == habit_id).first()
                        if habit is None:
                            print("Habit not found.")
                        else:
                            completions = db.query(Completion).filter(
                                Completion.habit_id == habit_id
                            ).all()
                            summary = build_habit_summary(habit, completions)
                            print("\nHABIT ANALYSIS")
                            print(f"Name: {summary['name']}")
                            print(f"Completed today: {summary['completed_today']}")
                            print(f"Current streak: {summary['current_streak']}")
                            print(f"Longest streak: {summary['longest_streak']}")
                            print(f"Total completions: {summary['total_completions']}")
                            print(f"Completion rate: {summary['completion_rate']}%")

                    elif analytics_choice == "5":
                        break
                    else:
                        print("Invalid analytics option.")

            elif choice == "8":
                try:
                    habit_id = int(input("Enter habit ID: "))

                    habit = (
                        db.query(Habit)
                        .filter(Habit.id == habit_id)
                        .first()
                    )

                    if habit is None:
                        print("Habit not found.")
                    else:
                        confirm = input(
                            f"Delete '{habit.name}'? (y/n): "
                        ).strip().lower()

                        if confirm == "y":
                            db.query(Completion).filter(
                                Completion.habit_id == habit_id
                            ).delete()

                            db.delete(habit)
                            db.commit()

                            print("Habit deleted successfully.")
                        else:
                            print("Deletion cancelled.")
                except ValueError:
                    print("Please enter a valid habit ID.")

            elif choice == "9":
                print("Goodbye!")
                break
            else:
                 print("Invalid option. Please choose a number from 1 to 9.")
    except ValueError:
        print("Please enter a valid habit ID.")
    finally:
        db.close()


if __name__ == "__main__":
    main()

# KADORA — Habit Tracking System

## 1. Project Overview

KADORA is a Python-based habit tracking application that helps users create habits, record completions, monitor streaks, and analyse their consistency over time.

The application provides two interfaces:
- A command-line interface (CLI).
- A REST API built with FastAPI.

## 2. Features

- Create, view, update, and delete habits.
- Organise habits by daily or weekly periodicity.
- Record habit completions.
- View completion history.
- Undo a completion recorded for the current day.
- Calculate current and longest streaks.
- View habit summaries and dashboard statistics.
- Filter habits by periodicity.
- Analyse the longest streak across all habits.
- Populate an empty database with demonstration data.

## 3. Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pytest

## 4. Project Structure

The project contains the following main components:

- `app/models/` — Defines the habit and completion database models.
- `app/services/` — Contains habit summary, streak calculation, and analytics logic.
- `app/database.py` — Configures the database connection and sessions.
- `app/main.py` — Defines the FastAPI application and API endpoints.
- `app/cli.py` — Provides the interactive command-line interface.
- `seed_data.py` — Populates the database with predefined habits and sample completion records.
- `tests/` — Contains automated tests.
- `requirements.txt` — Lists the Python dependencies.
- `README.md` — Provides project documentation.

## 5. Installation

### Prerequisites

Install Python and ensure it is available from your terminal.

### Step 1: Open the project directory

Open a terminal in the main KADORA project folder.

### Step 2: Create a virtual environment

Run:

    python -m venv .venv

### Step 3: Activate the virtual environment

On Windows PowerShell, run:

    .\.venv\Scripts\Activate.ps1

### Step 4: Install dependencies

Run:

    pip install -r requirements.txt

## 6. Database Setup

KADORA uses SQLite to store habits and their completion records.

The database connection is configured in `app/database.py`.

The application creates its database tables when the FastAPI application is loaded.

## 7. Running the Application

### Run the REST API

From the project root, run:

    uvicorn app.main:app --reload

Open the following address in your browser to access the interactive API documentation:

    http://127.0.0.1:8000/docs

### Run the command-line interface

Open a terminal in the project root and run:

    python -m app.cli

Follow the menu displayed in the terminal to manage habits and access analytics.

## 8. Demonstration Data

To populate an empty database with five predefined habits and four weeks of sample completion records, run:

    python seed_data.py

The script avoids inserting duplicate demonstration data when habits already exist in the database.

## 9. Running Tests

From the project root, run:

    python -m pytest -v

The automated tests check important application functionality and service logic.

## 10. Database Configuration

The default SQLite database URL is:

    sqlite:///./kadora.db

The database file is created relative to the application's working directory when SQLite connects to it.

## 11. Future Improvements

Potential improvements include:

- More comprehensive input validation.
- Better handling of duplicate completion attempts.
- Additional automated tests.
- More detailed analytics and reporting.
- A graphical user interface.
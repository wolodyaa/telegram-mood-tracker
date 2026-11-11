# 🤖 Telegram Mood Tracker

A Telegram bot for tracking daily mood. My first project in Aiogram with database integration and user registration.

## 🛠️ Tech Stack
* Python 3
* Aiogram 3 (asynchronous framework for Telegram bots)
* SQLite3 (built-in database for history storage)

## 🚀 Features
* User registration: saves user names to a separate `users` table for personalized greetings.
* `/start` command with dynamic main menu (registration or main menu depending on user status).
* `/help` command to explain bot features.
* Ability to log mood on a scale from 0 to 10 using a Finite State Machine (FSM).
* Saving mood history and user data to a SQLite database.
* Daily limit: prevents logging mood more than once a day.
* Viewing the last entry and average mood (for the last x days) via inline buttons.
* Protection against text input instead of numbers and valid range checking.

## 📂 Project Structure
* `main.py` — entry point, bot launch, and database initialization.
* `app/handlers.py` — command and message handlers.
* `app/database.py` — database functions (SQL queries for users and moods).
* `app/keyboards.py` — keyboards and buttons.
* `app/states.py` — FSM states for registration and mood logging.
* `config.py` — configuration file with the token and help text.

## ⚙️ How to run locally
1. Clone the repository.
2. Install dependencies: `pip install aiogram`
3. Create a `config.py` file in the root folder and add the following: 
   ```python
   TOKEN = "your_token_from_BotFather"
   DB_PATH = "moods.db"
   HELP_TEXT = "your help text here"

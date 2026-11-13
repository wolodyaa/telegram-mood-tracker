# 🤖 Telegram Mood Tracker

A Telegram bot for tracking daily mood. My first project built with Aiogram 3 and SQLite, featuring user registration, statistics, and robust error handling.

## 🛠️ Tech Stack
* Python 3
* Aiogram 3 (asynchronous framework for Telegram bots)
* SQLite3 (built-in database with relational tables for users and moods)

## 🚀 Features
* **User Registration:** Saves users to a separate `users` table to provide personalized greetings and track registration dates.
* `/start` command with dynamic routing (shows registration menu for new users, main menu for returning users).
* `/help` command to explain bot features.
* **Mood Logging:** Log mood on a scale from 0 to 10 using a Finite State Machine (FSM).
* **Daily Limit:** Prevents logging mood more than once a day.
* **Fallback Logic:** If an unregistered user logs a mood, the bot saves it but politely prompts them to register.
* **Statistics & Analytics:**
  * View the last logged mood.
  * View the average mood for the last 7 days.
  * View overall stats (total days logged, all-time average, and dynamic mood emojis).
* **Robust Error Handling:** Prevents crashes (`NoneType` errors) when data is missing or users interact with buttons without registering.

## 📂 Project Structure
* `main.py` — Entry point, bot launch, and database initialization.
* `app/handlers.py` — Command, message, and callback query handlers.
* `app/database.py` — Database functions (SQL queries for users and moods).
* `app/keyboards.py` — Reply and inline keyboards.
* `app/states.py` — FSM states for registration and mood logging.
* `config.py` — Configuration file with the bot token and help text.

## ⚙️ How to run locally
1. Clone the repository.
2. Install dependencies: `pip install aiogram`
3. Create a `config.py` file in the root folder and add the following: 
   ```python
   TOKEN = "your_token_from_BotFather"
   DB_PATH = "moods.db"
   HELP_TEXT = "your help text here"

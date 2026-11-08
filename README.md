# 🤖 Telegram Mood Tracker

A Telegram bot for tracking daily mood. My first project in Aiogram with database integration.

## 🛠️ Tech Stack
* Python 3
* Aiogram 3 (asynchronous framework for Telegram bots)
* SQLite3 (built-in database for history storage)

## 🚀 Features
* `/start` command and main menu.
* Ability to log mood on a scale from 0 to 10 using a Finite State Machine (FSM).
* Saving mood history to a SQLite database.
* Daily limit: prevents logging mood more than once a day.
* Viewing the last entry and average mood (for the last x days) via inline buttons.
* Protection against text input instead of numbers and valid range checking.

## 📂 Project Structure
* `main.py` — entry point, bot launch, and database initialization.
* `app/handlers.py` — command and message handlers.
* `app/database.py` — database functions (SQL queries).
* `app/keyboards.py` — keyboards and buttons.
* `config.py` — configuration file with the token.

## ⚙️ How to run locally
1. Clone the repository.
2. Install dependencies: `pip install aiogram`
3. Create a `config.py` file in the root folder and add the following: 
   `TOKEN = "your_token_from_BotFather"`
   `DB_PATH = "moods.db"`
4. Run the bot: `python main.py`

## 👨‍💻 Author
**Vladimir (wolodyaa)**
Beginner Python Developer.

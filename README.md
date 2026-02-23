# Telegram Productivity Bot for Software Engineers

This Telegram bot is designed to be a personal assistant for software engineers, helping to automate daily tasks and boost productivity. It leverages free-tier AI models to provide powerful features without any cost.

## Architecture

The bot is built with Python using the `python-telegram-bot` library. It uses a modular command-based architecture, making it easy to extend with new features.

- **`main.py`**: The main entry point of the application.
- **`bot/`**: The main package for the bot.
  - **`core/`**: Core components of the bot.
    - **`bot.py`**: Initializes the Telegram bot and registers command handlers.
    - **`config.py`**: Manages configuration and environment variables.
  - **`commands/`**: Contains the handlers for each bot command.
  - **`utils/`**: Utility modules, such as for interacting with AI APIs.

## Day 1 Features

- `/start`, `/help`: Display a welcome message and help text.
- `/ask`: Ask a question to the AI model.
- `/summarize`: Summarize text, articles, or code.
- `/debug`: Get help with debugging code.
- `/commit`: Generate a Git commit message.

## Free AI Services

This bot uses the [Groq API](https://groq.com/) for its AI capabilities. Groq provides fast inference with a generous free tier, making it ideal for this project.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd telegram-productivity-bot
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set up your Telegram bot:**
    - Talk to the [@BotFather](https://t.me/BotFather) on Telegram to create a new bot.
    - Copy the bot token you receive.

4.  **Get your Groq API key:**
    - Sign up for a free account at [Groq](https://console.groq.com/).
    - Create an API key.

5.  **Configure environment variables:**
    - Create a `.env` file in the root of the project.
    - Add the following variables:
      ```
      TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
      GROQ_API_KEY="your_groq_api_key"
      ```

6.  **Run the bot:**
    ```bash
    python main.py
    ```

# 🤖 Telegram Productivity Bot for Software Engineers

A personal AI-powered Telegram bot designed to boost productivity for software engineering students and developers. Built with Python, powered by Google Gemini AI.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=flat&logo=telegram)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-orange?style=flat&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)

---

## ✨ Features

| Command | Description |
|---|---|
| `/summarize` | Summarize any text into clear bullet points |
| `/prompt` | Generate structured AI prompts using RTF framework |
| `/git` | Generate professional Conventional Commit messages |
| `/debug` | Analyze error logs and get 3-step fix suggestions |
| `/explain` | Explain any code or concept in simple terms |
| `/tip` | Get a daily software engineering tip |
| `/todo` | Manage a personal task list |
| `/plan` | Format your daily goals into a structured plan |
| `/save` | Save notes to a personal knowledge base |
| `/ask` | Query your saved knowledge base with AI |

---

## 🏗️ Architecture

```
TelegramBot/
├── main.py                  # Entry point & handler registration
├── requirements.txt         # Dependencies
├── .env                     # Environment variables (not committed)
└── bot/
    ├── commands/            # Command handlers
    │   ├── start.py         # /start command & keyboard
    │   ├── summarize.py     # /summarize command
    │   ├── prompt.py        # /prompt command
    │   ├── eng_tools.py     # /git and /debug commands
    │   ├── explain.py       # /explain command
    │   ├── tip.py           # /tip command
    │   ├── todo.py          # /todo command
    │   ├── plan.py          # /plan command
    │   ├── kb_handler.py    # /save and /ask commands
    │   └── image_handler.py # Image analysis
    ├── core/
    │   └── config.py        # Configuration & env variables
    └── utils/
        ├── ai_utils.py      # Gemini AI integration
        └── knowledge_base.txt # Local knowledge base storage
```

---

## 🛠️ Tech Stack

- **Runtime:** Python 3.10+
- **Bot Framework:** [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v22
- **AI Model:** Google Gemini 2.5 Flash
- **Scheduler:** APScheduler
- **Keep-alive:** Flask
- **Hosting:** Render (Free tier)
- **Uptime Monitoring:** UptimeRobot

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)
- A Google Gemini API Key from [Google AI Studio](https://aistudio.google.com)

### 1. Clone the Repository
```bash
git clone https://github.com/kallzth/TelegramBot.git
cd TelegramBot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Run the Bot
```bash
python main.py
```

---

## ☁️ Deployment

This bot is deployed on **Render** with **UptimeRobot** keeping it alive 24/7.

### Deploy on Render
1. Fork this repository
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repo
4. Set environment variables in Render dashboard
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python main.py`

---

## 📋 Usage Examples

**Generate a git commit message:**
```
/git I added JWT authentication to the login endpoint
```

**Summarize text:**
```
/summarize [paste any long text here]
```

**Explain a concept:**
```
/explain what is Big O notation
```

**Manage your todo list:**
```
/todo add Study binary trees
/todo done 1
/todo
```

**Format daily goals:**
```
/plan Study data structures, Fix login bug, Read Clean Code
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from BotFather | ✅ Yes |
| `GEMINI_API_KEY` | Google Gemini API key from AI Studio | ✅ Yes |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Kaleab Zelalem**
- GitHub: [@kallzth](https://github.com/kallzth)
- Built as a personal productivity tool for software engineering students

---

⭐ If you found this useful, please give it a star!

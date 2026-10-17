# Telegram Music bot
A Telegram bot that finds songs on YouTube and sends them as audio.
Built with Python as a personal learning project.

## Features
- Send a song name, get the audio back
- Searches YouTube using yt-dlp
- Friendly error message if a song is not found
- Bot token is stored safely in a `.env` file

## Tech Stack
- Python 3
- python-telegram-bot
- yt-dlp
- python-dotenv

## How to Run
1. Install the libraries:
 `pip install python-telegram-bot yt-dlp python-dotenv`
2. Create a bot with @BotFather on Telegram and copy the token.
3. Create a `.env` file in the project folder:
 `BOT_TOKEN=your_token_here`
4. Start the bot:
 `py bot.py`

## What I Learned
- Working with the Telegram Bot API
- Handling errors and logging
- Keeping secrets out of code with environment variables

## Author
Kamolov Doston

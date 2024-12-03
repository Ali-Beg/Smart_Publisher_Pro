import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# API Configuration
GEMINI_API_KEYS = os.getenv('GEMINI_API_KEYS', '').split(',')
if not GEMINI_API_KEYS or GEMINI_API_KEYS[0] == '':
    raise ValueError("GEMINI_API_KEYS environment variable is not set")

# Telegram Configuration - Use raw values for testing
# TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'xxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
# TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-xxxxxxxxxxx')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Validate Telegram configuration
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Telegram configuration is incomplete")

# App Settings
MAX_RETRIES = 5
INITIAL_BACKOFF = 1
MAX_CONTENT_LENGTH = 4000
INTRO_LENGTH = 2000
CONCLUSION_LENGTH = 2000
import requests
import time
import streamlit as st
from typing import List, Dict
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from config.settings import MAX_RETRIES

def send_to_telegram(summaries: List[Dict], max_retries=MAX_RETRIES) -> bool:
    """Send summaries to Telegram with retry mechanism"""
    try:
        message = "📚 <b>Today's Article </b>\n\n"
        for idx, item in enumerate(summaries, 1):
            message += f"#{idx} 📌 <b>{item['title']}</b>\n\n"
            message += f"📝 {item['summary']}\n\n"
            message += "──────────────────\n\n"
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": TELEGRAM_CHAT_ID,
                        "text": message,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True
                    },
                    timeout=10
                )
                return response.status_code == 200
            except requests.exceptions.RequestException:
                if attempt == max_retries - 1:
                    return False
                time.sleep(2 ** attempt)
        
        return False
    except Exception as e:
        st.error(f"Error sending to Telegram: {str(e)}")
        return False
import os
import requests
from typing import Optional, Dict, Any


class TelegramClient:
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(
        self, chat_id: str, text: str, parse_mode: str = "HTML"
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}

        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def format_post(self, post: Dict[str, Any]) -> str:
        url = post.get("url", "")

        message = "New Post\n\n\n"
        if url:
            message += url

        return message

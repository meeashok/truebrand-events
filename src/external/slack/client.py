import os
from slack.web.client import WebClient


class SlackWrapper:
    @staticmethod
    def send_message(message: str, channel: str = "general"):
        token = os.getenv('SLACK_BOT_TOKEN')
        if not token:
            raise ValueError("SLACK_BOT_TOKEN environment variable is required")
        
        client = WebClient(token=token)
        client.chat_postMessage(channel=channel, text=message)  # type:ignore
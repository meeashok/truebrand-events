import json
import os
from dotenv import load_dotenv
from src.external.typefully import TypefullyClient
from src.external.telegram import TelegramClient

# Load environment variables
load_dotenv()


# Configuration for multiple accounts
ACCOUNTS = [
    {
        "typefully_api_key": "NdwJTmEDxuWNUtR3",
        "typefully_username": "Devin",
        "telegram_chat_id": "-4714539400",
    },
    {
        "typefully_api_key": "qoOjuNhLWNYp43ot",
        "typefully_username": "Avani",
        "telegram_chat_id": "-4714539400",
    },
    {
        "typefully_api_key": "SII4NCH1KtpBgDjU",
        "typefully_username": "SoloTech",
        "telegram_chat_id": "-4714539400",
    },
    # Add more accounts here
    # {
    #     'name': 'Account 2',
    #     'typefully_api_key': 'another_api_key',
    #     'telegram_chat_id': 'another_chat_id',
    #     'slack_channel': '#general'  # Future integrations
    # },
]


def get_telegram_chat_name(chat_id: str) -> str:
    """Fetch telegram chat name from API"""
    if not chat_id:
        return "Unknown"

    try:
        telegram = TelegramClient()
        chat_info = telegram.get_chat_info(chat_id)
        return chat_info.get("result", {}).get("title", "Unknown")
    except Exception as e:
        print(f"Failed to fetch Telegram chat name: {e}")
        return "Unknown"


def fetch_typefully_posts(api_key: str, minutes: int = 2) -> list:
    """Fetch recent posts from Typefully"""
    typefully = TypefullyClient(api_key)
    return typefully.fetch_recent_posts(minutes=minutes)


def send_posts_to_telegram(posts: list, chat_id: str, typefully_username: str) -> int:
    """Send posts to Telegram and return count of sent messages"""
    if not posts or not chat_id:
        return 0

    telegram = TelegramClient()
    sent_count = 0

    for post in posts:
        url = post.get("url", "")
        # Only send if it's an x.com post
        if url and "x.com" in url:
            try:
                message = telegram.format_post(post)
                telegram.send_message(chat_id, message)
                sent_count += 1
            except Exception as e:
                print(
                    f"[{typefully_username}] Failed to send post {post.get('id')}: {e}"
                )

    return sent_count


def process_account(account):
    """Process a single account"""
    telegram_chat_id = account.get("telegram_chat_id")
    typefully_username = account.get("typefully_username", "Unknown")

    # Test mode: override chat ID
    test_mode = os.environ.get("TEST_MODE", "").lower() == "true"
    if test_mode:
        telegram_chat_id = "-4715482029"  # Test chat
        print(f"TEST MODE: Using chat ID {telegram_chat_id}")

    # Get chat name and log processing info
    telegram_chat_name = get_telegram_chat_name(telegram_chat_id)
    print(
        f"Processing: {typefully_username} → {telegram_chat_name} ({telegram_chat_id})"
    )

    try:
        # Step 1: Fetch posts from Typefully
        posts = fetch_typefully_posts(account["typefully_api_key"], minutes=2)

        if not posts:
            return {
                "account": f"{typefully_username}",
                "status": "success",
                "posts_found": 0,
                "posts_sent": 0,
            }

        # Step 2: Send to Telegram
        sent_count = send_posts_to_telegram(posts, telegram_chat_id, typefully_username)

        # Future integrations can be added here:
        # if account.get('slack_channel'):
        #     send_to_slack(posts, account['slack_channel'])

        return {
            "account": f"{typefully_username}",
            "status": "success",
            "posts_found": len(posts),
            "posts_sent": sent_count,
        }

    except Exception as e:
        return {
            "account": f"{typefully_username}",
            "status": "error",
            "message": str(e),
        }


def lambda_handler(event, context):
    results = []

    for account in ACCOUNTS:
        result = process_account(account)
        results.append(result)
        print(f"Processed {result}")

    total_found = sum(r.get("posts_found", 0) for r in results)
    total_sent = sum(r.get("posts_sent", 0) for r in results)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "total_posts_found": total_found,
                "total_posts_sent": total_sent,
                "results": results,
            }
        ),
    }


if __name__ == "__main__":
    lambda_handler({}, None)

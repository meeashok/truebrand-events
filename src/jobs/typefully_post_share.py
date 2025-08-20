import json
from dotenv import load_dotenv
from src.external.typefully import TypefullyClient
from src.external.telegram import TelegramClient

# Load environment variables
load_dotenv()


# Configuration for multiple accounts
ACCOUNTS = [
    {
        "name": "Quantplay AI",
        "typefully_api_key": "NdwJTmEDxuWNUtR3",
        "telegram_chat_id": "-4715482029",
    },
    # Add more accounts here
    # {
    #     'name': 'Account 2',
    #     'typefully_api_key': 'another_api_key',
    #     'telegram_chat_id': 'another_chat_id',
    #     'slack_channel': '#general'  # Future integrations
    # },
]


def process_account(account):
    """Process a single account"""
    name = account.get("name", "Unknown")

    try:
        # Step 1: Fetch posts from Typefully
        typefully = TypefullyClient(account["typefully_api_key"])
        posts = typefully.fetch_recent_posts(minutes=2)  # 2 minutes

        if not posts:
            return {
                "account": name,
                "status": "success",
                "posts_found": 0,
                "posts_sent": 0,
            }

        # Step 2: Send to Telegram
        sent_count = 0
        if account.get("telegram_chat_id"):
            telegram = TelegramClient()
            for post in posts:
                try:
                    message = telegram.format_post(post)
                    telegram.send_message(account["telegram_chat_id"], message)
                    sent_count += 1
                except Exception as e:
                    print(f"[{name}] Failed to send post {post.get('id')}: {e}")

        # Future integrations can be added here:
        # if account.get('slack_channel'):
        #     send_to_slack(posts, account['slack_channel'])

        return {
            "account": name,
            "status": "success",
            "posts_found": len(posts),
            "posts_sent": sent_count,
        }

    except Exception as e:
        return {"account": name, "status": "error", "message": str(e)}


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

# Truebrand Events - Typefully Post Sharing System

## Overview
Automated system that fetches recent posts from Typefully and shares them to Telegram. Deployed as AWS Lambda function for serverless execution.

## Architecture
- **Lambda Function**: `TruebrandPostShare` (Ireland/eu-west-1)
- **Handler**: `src.jobs.typefully_post_share.lambda_handler`
- **Time Window**: Last 2 minutes (configurable)
- **Integrations**: Typefully API → Telegram Bot API

## Project Structure
```
src/
├── external/
│   ├── typefully/
│   │   ├── __init__.py
│   │   └── client.py          # TypefullyClient - fetches posts
│   ├── telegram/
│   │   ├── __init__.py
│   │   └── client.py          # TelegramClient - sends messages
│   └── slack/
│       ├── __init__.py
│       └── client.py          # SlackWrapper - future integration
└── jobs/
    └── typefully_post_share.py # Main Lambda handler
```

## Configuration
Account settings in `src/jobs/typefully_post_share.py`:
```python
ACCOUNTS = [
    {
        'name': 'Quantplay AI',
        'typefully_api_key': 'NdwJTmEDxuWNUtR3',
        'telegram_chat_id': '-4715482029'
    }
]
```

## Environment Variables
**Required in AWS Lambda:**
- `TELEGRAM_BOT_TOKEN`: `7830201804:AAGu_eX7rCSEG40FJCrJoMpBo2mbfBZCdRI`

## Message Format
Telegram messages sent as:
```
New Post

https://x.com/toolandtea/status/[post_id]
```

## Local Development
```bash
# Install dependencies
pipenv install

# Test locally
pipenv run python -m src.jobs.typefully_post_share

# Expected output: {'account': 'Quantplay AI', 'status': 'success', 'posts_found': X, 'posts_sent': X}
```

## Deployment
```bash
# Deploy to AWS Lambda
./deploy.sh TruebrandPostShare

# Function deployed to: eu-west-1 (Ireland)
# Updates both code and dependencies
```

## API Endpoints Used
- **Typefully**: `https://api.typefully.com/v1/drafts/recently-published/`
  - Header: `X-API-KEY: Bearer {api_key}`
- **Telegram**: `https://api.telegram.org/bot{token}/sendMessage`

## Time Configuration
To change time window, edit `src/jobs/typefully_post_share.py`:
```python
posts = typefully.fetch_recent_posts(minutes=2)  # Change this value
```

## Current Status
- ✅ Deployed and functional
- ✅ Fetches posts from last 2 minutes  
- ✅ Sends to Telegram group "Quantplay AI assistant"
- ✅ Simple, concise codebase (~90 lines)

## Future Integrations
- Slack integration ready (SlackWrapper created)
- Add accounts by extending ACCOUNTS list
- CloudWatch scheduling for automation
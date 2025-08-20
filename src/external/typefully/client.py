import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any


class TypefullyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.typefully.com/v1"
        self.headers = {
            "X-API-KEY": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def fetch_recent_posts(self, minutes: int = 1) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/drafts/recently-published/"
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Handle if response is directly a list or has a 'data' key
        if isinstance(data, list):
            posts = data
        else:
            posts = data.get('data', data.get('results', []))
        
        recent_posts = []
        for post in posts:
            # Use the correct field name from API response
            published_at = post.get('published_on')
            if published_at:
                try:
                    post_time = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    if post_time > cutoff_time:
                        recent_posts.append({
                            'title': post.get('text_first_tweet', '')[:100] + '...' if len(post.get('text_first_tweet', '')) > 100 else post.get('text_first_tweet', ''),
                            'content': post.get('text_first_tweet', ''),
                            'url': post.get('twitter_url', ''),
                            'id': post.get('id', '')
                        })
                except Exception as e:
                    print(f"Error parsing date {published_at}: {e}")
        
        return recent_posts
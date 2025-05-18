import os
import requests

API_KEY = os.environ['NEWSAPI_KEY']
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_USER_ID = os.environ['LINE_USER_ID']

def send_line_bot(message, user_id, access_token):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    body = {
        "to": user_id,
        "messages": [
            {"type": "text", "text": message}
        ]
    }
    requests.post(url, headers=headers, json=body)

print('---今日の記事---')
url = f'https://newsapi.org/v2/top-headlines?language=en&country=us&pageSize=5&apiKey={API_KEY}'
response = requests.get(url)
data = response.json()

if data.get("status") != "ok":
    print("エラー:", data)
else:
    articles = data.get("articles", [])
    if not articles:
        msg = "該当する英語記事はありません。"
    else:
        msg = '---今日の英語ニュース---\n'
        for article in articles:
            msg += f"\n{article['title']}\n{article['url']}\n{article['description']}\n"
    # LINEに送信
    send_line_bot(msg, LINE_USER_ID, LINE_CHANNEL_ACCESS_TOKEN)

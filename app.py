import os
from flask import Flask, render_template
import feedparser
from datetime import datetime, timedelta
import time

# Flask가 template 폴더를 절대 경로로 정확히 찾도록 설정합니다.
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

def get_news():
    # URL 주소에 대괄호([])가 없는지 꼭 확인하세요!
    rss_url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    
    news_list = []
    last_24h = datetime.now() - timedelta(days=1)

    for entry in feed.entries:
        published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        if published_time > last_24h:
            news_list.append({
                'title': entry.title,
                'link': entry.link,
                'date': published_time.strftime('%Y-%m-%d %H:%M')
            })
    return news_list[:10]

@app.route('/')
def home():
    news_data = get_news()
    return render_template('index.html', news=news_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
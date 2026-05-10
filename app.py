import os
import re
import html  # HTML 특수문자 변환을 위해 추가
from flask import Flask, render_template
import feedparser
from datetime import datetime, timedelta
import time

base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

def clean_html(raw_html):
    """HTML 태그를 제거하고 &nbsp; 같은 엔티티를 문자로 변환"""
    if not raw_html:
        return ""
    
    # 1. &nbsp; &middot; 등을 실제 문자로 변환
    decoded_text = html.unescape(raw_html)
    
    # 2. <태그> 제거
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', decoded_text)
    
    # 3. 양끝 공백 정리
    return cleantext.strip()

def get_news():
    rss_url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    
    news_list = []
    last_24h = datetime.now() - timedelta(days=1)

    for entry in feed.entries:
        # 뉴스 발행 시간 파싱
        published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        
        if published_time > last_24h:
            # 요약문 가져오기 및 청소
            summary = getattr(entry, 'summary', '요약 내용이 없습니다.')
            clean_summary = clean_html(summary)
            
            news_list.append({
                'title': html.unescape(entry.title), # 제목에도 특수문자가 있을 수 있어 적용
                'link': entry.link,
                'date': published_time.strftime('%Y-%m-%d %H:%M'),
                'summary': clean_summary[:150] + "..." if len(clean_summary) > 150 else clean_summary
            })
            
    return news_list[:10]

@app.route('/')
def home():
    news_data = get_news()
    return render_template('index.html', news=news_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
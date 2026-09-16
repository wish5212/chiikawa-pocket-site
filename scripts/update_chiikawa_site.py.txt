#!/usr/bin/env python3
import datetime as dt
import email.utils
import html
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# --- 設定項目 ---
# ※セキュリティのため、認証情報はGitHubの「Secrets」から読み込む形にしています。
WP_URL = os.environ.get('WP_URL')          # 例: https://your-site.com
WP_USER = os.environ.get('WP_USER')        # WordPressのユーザー名
WP_PASSWORD = os.environ.get('WP_PASSWORD')  # 先ほど発行したアプリケーションパスワード

QUERY = 'ちいかわ'
RSS_URL = 'https://news.google.com/rss/search?q=' + urllib.parse.quote(QUERY) + '&hl=ja&gl=JP&ceid=JP:ja'
USER_AGENT = 'Mozilla/5.0 (compatible; chiikawa-pages-updater/1.0; +https://github.com/)'
MAX_ITEMS = 12

CATEGORY_RULES = [
    ('goods', 'グッズ', ['グッズ', 'ぬいぐるみ', 'マスコット', 'マーケット', '商品', '発売', 'ワッフル', 'シール', 'パン', 'ベーカリー', 'プライズ', 'バッグ']),
    ('collab', 'コラボ', ['コラボ', 'コラボレーション', 'くら寿司', 'ファミマ', 'キャンペーン', 'カフェ']),
    ('anime', 'アニメ・映画', ['アニメ', '映画', '放送', '公開', '劇場', 'エピソード', '上映']),
    ('event', 'イベント', ['イベント', 'フェア', 'まつり', '展示', '夏まつり', '予約', 'ショップ']),
]

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', 'ignore')

def clean_text(text: str) -> str:
    if not text:
        return ''
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_date(raw: str):
    if not raw:
        return None
    try:
        return email.utils.parsedate_to_datetime(raw)
    except Exception:
        return None

def classify(title: str, snippet: str):
    joined = f'{title} {snippet}'
    for key, label, keywords in CATEGORY_RULES:
        if any(word in joined for word in keywords):
            return key, label
    return 'other', 'そのほか'

def parse_items(xml_text: str):
    root = ET.fromstring(xml_text)
    channel = root.find('channel')
    results = []
    seen = set()
    if channel is None:
        return results
    for item in channel.findall('item'):
        title = clean_text(item.findtext('title', default=''))
        link = clean_text(item.findtext('link', default=''))
        raw_date = clean_text(item.findtext('pubDate', default=''))
        description = clean_text(item.findtext('description', default=''))
        source_el = item.find('source')
        source = clean_text(source_el.text if source_el is not None and source_el.text else '') or 'Google ニュース'
        if not title or not link:
            continue
        
        # 重複チェック用の一意のキー
        norm_title = re.sub(r'\W+', '', title)
        key = norm_title.lower()[:100] + '|' + link.split('?')[0]
        if key in seen:
            continue
        seen.add(key)
        
        category_key, category_label = classify(title, description)
        published = parse_date(raw_date)
        if published and published.tzinfo is None:
            published = published.replace(tzinfo=dt.timezone.utc)
        
        if published:
            jst = published.astimezone(dt.timezone(dt.timedelta(hours=9)))
            published_iso = jst.isoformat()
        else:
            published_iso = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).isoformat()

        results.append({
            'title': title,
            'link': link,
            'source': source,
            'snippet': description,
            'category_label': category_label,
            'published_at': published_iso,
        })
    results.sort(key=lambda x: x['published_at'], reverse=True)
    return results[:MAX_ITEMS]

def post_to_wordpress(item):
    """WordPressに記事を自動投稿する関数"""
    if not WP_URL or not WP_USER or not WP_PASSWORD:
        print("WordPressの連携情報が設定されていないため、投稿をスキップします。")
        return

    # 投稿する内容を作成
    api_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"
    
    # 記事本文（HTML）を作成
    content_html = f"""
    <p>{item['snippet']}</p>
    <p>情報元: <a href="{item['link']}" target="_blank" rel="noopener">{item['source']}</a></p>
    <p>カテゴリー: {item['category_label']}</p>
    """

    payload = {
        'title': item['title'],
        'content': content_html,
        'status': 'publish', # すぐに公開状態にする
    }
    
    # 認証情報の作成（Basic認証）
    import base64
    auth_string = f"{WP_USER}:{WP_PASSWORD}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        api_url,
        data=req_data,
        headers={
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT
        }
    )
    
    try:
        # 重複投稿を避けるため、同じタイトルの記事がないかチェックするのが理想ですが、
        # まずはシンプルに新規作成のリクエストを送信します。
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 201:
                print(f"成功: 「{item['title']}」をWordPressに投稿しました。")
    except Exception as e:
        print(f"エラー: {item['title']} の投稿に失敗しました。理由: {e}")

def main():
    print("Googleニュースから『ちいかわ』の最新情報を取得中...")
    xml_text = fetch(RSS_URL)
    items = parse_items(xml_text)
    
    print(f"最新のニュースを {len(items)} 件取得しました。WordPressへの同期を開始します。")
    for item in items:
        post_to_wordpress(item)
        
    print("すべての処理が完了しました。")

if __name__ == '__main__':
    main()
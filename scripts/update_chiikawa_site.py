#!/usr/bin/env python3
import datetime as dt
import email.utils
import html
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
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

TARGET_HTMLS = [
    BASE / 'chiikawa-fansite.html',
    BASE / 'chiikawa-fansite-edited.html',
    BASE / 'index.html',
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


def summarize(snippet: str, source: str, category_label: str) -> str:
    base = clean_text(snippet)
    if not base:
        return f'{source}が伝えた{category_label}の話題です。'
    if len(base) > 96:
        base = base[:96].rstrip(' 、。') + '…'
    return base


def unique_key(title: str, link: str) -> str:
    norm_title = re.sub(r'\W+', '', title)
    return norm_title.lower()[:100] + '|' + link.split('?')[0]


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
        key = unique_key(title, link)
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
            published_display = jst.strftime('%Y-%m-%d %H:%M JST')
        else:
            published_iso = ''
            published_display = ''
        results.append({
            'title': title,
            'link': link,
            'source': source,
            'snippet': description,
            'summary': summarize(description, source, category_label),
            'category_key': category_key,
            'category_label': category_label,
            'published_at': published_iso,
            'published_display': published_display,
        })
    results.sort(key=lambda x: x['published_at'], reverse=True)
    return results[:MAX_ITEMS]


def build_payload(items):
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    counts = Counter(item['category_key'] for item in items)
    labels = {key: label for key, label, _ in CATEGORY_RULES}
    labels['other'] = 'そのほか'
    categories = [
        {
            'key': key,
            'label': labels[key],
            'count': counts.get(key, 0),
            'icon': {'goods': '🎀', 'collab': '🍰', 'anime': '🎬', 'event': '🌟', 'other': '🌱'}[key],
        }
        for key in ['goods', 'collab', 'anime', 'event', 'other']
        if counts.get(key, 0)
    ]
    return {
        'site_title': 'ちいかわぽけっと',
        'query': QUERY,
        'generated_at': now.isoformat(),
        'generated_at_jst': now.strftime('%Y-%m-%d %H:%M JST'),
        'update_interval_hours': 12,
        'sources': [
            {'name': 'Google ニュース 検索RSS', 'url': RSS_URL}
        ],
        'categories': categories,
        'items': items,
    }


def inject_payload(html_text: str, payload: dict) -> str:
    replacement = '<script id="embedded-data" type="application/json">' + json.dumps(payload, ensure_ascii=False, indent=2) + '</script>'
    updated, count = re.subn(
        r'<script id="embedded-data" type="application/json">.*?</script>',
        replacement,
        html_text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError('embedded-data script tag not found')
    return updated


def main():
    xml_text = fetch(RSS_URL)
    items = parse_items(xml_text)
    payload = build_payload(items)

    (BASE / 'data.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

    source_html = TARGET_HTMLS[0].read_text(encoding='utf-8')
    updated_html = inject_payload(source_html, payload)
    for path in TARGET_HTMLS:
        path.write_text(updated_html, encoding='utf-8')

    print(f'updated {len(items)} items')
    print('targets:')
    for path in TARGET_HTMLS:
        print(path.name)


if __name__ == '__main__':
    main()

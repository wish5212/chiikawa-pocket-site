# Handoff: ちいかわぽけっと (Chiikawa Fansite)

## Overview
「ちいかわぽけっと」は、キャラクター『ちいかわ』に関するニュース（グッズ、コラボ、アニメ・映画、その他話題）を、複数の情報源（Google ニュース検索 RSS など）から自動収集し、カテゴリ判定・要約・重複除去したうえで、半日ごとに自動更新して公開する、ファン向けの非公式まとめサイトです。

このデザインの主な狙い：
- 一般の訪問者（ちいかわファン）が楽しく閲覧できるポップ／かわいいトーンにする
- カテゴリ別に切り替えて最新ニュース一覧を閲覧できる
- 「人気ランキング」「カテゴリガイド」で回遊性を上げる
- 各記事は要約＋出典リンクのみを掲載し、本文は転載しない（送客型メディア）

## About the Design Files
このバンドルに含まれる HTML ファイルは、**HTML で作成した“デザインリファレンス”**（見た目とふるまいを示すプロトタイプ）です。プロダクションコードとしてそのまま流用することは想定していません。

エンジニアの作業は、これらの HTML デザインを、**ターゲットとなるコードベースの既存環境**（Next.js / React / Vue / Astro / SvelteKit などの静的サイト生成基盤や、既存の CMS / RSS 収集バッチと組み合わせるなど）で **再現**することです。まだフレームワークが未選定であれば、以下の性質を踏まえて最適な構成を選んでください：

- ページ本体はほぼ静的（半日に 1 回のバッチ更新）→ **静的サイト生成 (SSG) が最適**
- クライアント側での重い状態管理は不要（カテゴリフィルタと軽い装飾のみ）
- ホスティングは Cloudflare Pages / Vercel / Netlify / GitHub Pages などを想定
- データソースは Google ニュース検索 RSS を起点に、他ソースを増減できる設計

推奨スタックの一例：
- **Astro** or **Next.js (App Router, SSG)** で静的書き出し
- ニュース収集バッチは Node.js / Python を GitHub Actions で 12 時間おきに実行し、`items.json` を生成
- ビルド時にその JSON を読み込んで静的 HTML を生成
- CSS は Tailwind でも素の CSS でも可（本モックは素の CSS）

## Fidelity
**High-fidelity (hifi)** です。カラー、タイポグラフィ、余白、角丸、シャドウ、装飾、インタラクションを含めて、**そのままピクセルパーフェクトで再現**することを想定してください。ロゴマークやミニキャラのビジュアルは CSS のみで描画されており、そのまま流用可能です。

## Screens / Views

このデザインは**シングルページ**構成です。上から順に以下のセクションが縦に並びます。

### 1. Navbar（サイト共通ヘッダー）
- **Purpose**: ロゴとサイトナビゲーション、更新頻度バッジ
- **Layout**:
  - `max-width: 1180px`、中央寄せ、水平パディング 20px
  - 白背景の pill 型（`border-radius: 999px`）、`border: 3px solid #fff`、下シャドウ `0 8px 24px rgba(198,138,130,0.14)`
  - 内部は `display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 14px 22px`
- **Components**:
  - **ロゴ**（左）:
    - テキスト「ちいかわぽけっと」フォント `Zen Maru Gothic 900 / 22px`、色 `#4a3630`
    - 隣に円形ロゴマーク（40×40、`border-radius: 50%`、背景 `linear-gradient(135deg, #fff0dc 0%, #ffe0c2 100%)`、`border: 3px solid #fff`、`box-shadow: 0 4px 0 #ffe1ec`）
    - ロゴマーク内に CSS で目・ほっぺ・口を描画（`::before` `::after` および子 span を使用。詳細は HTML の `.logo-mark` を参照）
  - **ナビメニュー**（中央）: 「最新まとめ」「人気ランキング」「カテゴリ」の 3 リンク
    - フォント `M PLUS Rounded 1c 700 / 14px`、色 `#6b4f47`
    - パディング `8px 14px`、`border-radius: 999px`
    - ホバー: 背景 `#ffe1ec`、文字色 `#ff6ea3`
  - **右バッジ**: 「♡ 毎日おかわり更新」
    - 背景 `linear-gradient(135deg, #ffd970 0%, #ffb08c 100%)`、色 `#7a4a1a`
    - `padding: 8px 14px`、`border-radius: 999px`、`box-shadow: 0 3px 0 rgba(255,143,90,0.35)`
    - フォント `M PLUS Rounded 1c 800 / 13px`

### 2. Hero
- **Purpose**: サイトの世界観とキャッチコピー、主要メトリクス、今日の気分バナー
- **Layout**:
  - 白背景、`border: 4px solid #fff`、`border-radius: 40px`、`padding: 40px 40px 34px`
  - シャドウ `0 10px 0 rgba(255,143,184,0.18), 0 20px 40px rgba(255,143,184,0.15)`
  - 内部 grid: `grid-template-columns: 1.4fr 1fr; gap: 28px; align-items: center`
  - 背景装飾レイヤ（`.hero-bg`）: `radial-gradient` を 4 つ重ねてパステルの丸を四隅に配置。詳細は HTML の CSS を参照
- **Components (左カラム)**:
  - **eyebrow-cute**: テキスト `✦ CHIIKAWA POCKET ✦`
    - 背景 `#ff8fb8`、色 `#fff`、パディング `7px 16px`、`border-radius: 999px`
    - `box-shadow: 0 3px 0 #ff6ea3`、`transform: rotate(-2deg)`
    - フォント 800 / 13px
  - **h1**: 「きょうの**ちいかわ**、\nぜんぶここに**♡**」
    - フォント `Zen Maru Gothic 900`、サイズ `clamp(36px, 5.4vw, 62px)`、`line-height: 1.08`、`letter-spacing: -0.02em`、色 `#4a3630`
    - 「ちいかわ」に黄色マーカー（`background: linear-gradient(180deg, transparent 60%, #ffd970 60%)`）
    - 「♡」は色 `#ff6ea3`、1.4s ease-in-out infinite のハートビートアニメ（`scale 1 → 1.18 → 1`）
  - **hero-lead**（本文）:
    ```
    ちいかわ・ハチワレ・うさぎのグッズ情報、コラボカフェ、映画・アニメ、
    ちょっとほっこりする話題まで。ネットのちいかわニュースをぎゅーっとまとめて、
    半日ごとにおかわり更新でお届けするよ！
    ```
    - フォント 500 / 15.5px、`line-height: 1.95`、色 `#6b4f47`、`max-width: 480px`
  - **m-chip（メトリクスチップ）4 個**（横並び、`gap: 10px`、`flex-wrap: wrap`）:
    | # | 数字 | ラベル | ボーダー / 影 |
    |---|------|--------|----------------|
    | 1 | 今日のトピック件数（動的） | 今日のトピック | `#ffe1ec` |
    | 2 | グッズ件数（動的） | グッズ情報 | `#d4f5e8` |
    | 3 | アニメ・映画件数（動的） | アニメ・映画 | `#fff2c4` |
    | 4 | `12h` | おかわり間隔 | `#ece2ff` |
    - 各チップ: 白背景、`border: 2px solid <色>`、`border-radius: 18px`、`padding: 10px 14px`、`box-shadow: 0 4px 0 <同色>`
    - 数字は `Fredoka 700 / 26px`、ラベルは `M PLUS Rounded 1c 700 / 11px`、色 `#9c8078`
- **Components (右カラム: メインビジュアル)**:
  - 正方形 `aspect-ratio: 1/1`、最大 340px、右寄せ
  - **雲**（`.mv-cloud`）: 白い丸＋`::before` `::after` で上部に 2 つのコブ、インセット下シャドウで陰影
  - **顔**（`.mv-face`）: ちいかわ風ミニキャラ。ベージュのグラデ楕円＋耳 2 つ＋目 2 つ＋ほっぺ 2 つ＋口 1 つを CSS のみで描画。詳細は HTML の `.mv-face`
  - **キラキラ 3 個**（`.sparkle.s1/s2/s3`）: `✧` `✦` `✧` を絶対配置、それぞれ黄色 / 濃ピンク / ミント
  - **NEW バッジ**（`.heart-badge`）: 円形 62×62、背景 `#ff8fb8`、色 `#fff`、`transform: rotate(10deg)`、`box-shadow: 0 5px 0 #ff6ea3`、テキスト「NEW\n♡」
- **Mood Bar**（Hero の下端に配置）:
  - `margin-top: 22px`、パディング `14px 20px`、`border: 3px dashed #fff`、`border-radius: 999px`
  - 背景 `linear-gradient(135deg, #fff2c4 0%, #ffe1ec 100%)`
  - 中央寄せ、内容: `[きょうの気分] [<mood>] な話題がいっぱい♡`
  - `<mood>` は `["わくわく","ほくほく","きゅん","うるうる","にっこり","もぐもぐ","ふわふわ"]` から更新時刻＋件数のシードで決定的に 1 つ選ぶ

### 3. Side Row（人気ランキング＋カテゴリガイド）
- **Layout**: `grid-template-columns: 1.1fr 1fr; gap: 20px; margin-top: 44px`
- **共通の box スタイル**: 白背景、`border: 3px solid #fff`、`border-radius: 32px`、`padding: 26px 26px 24px`、`box-shadow: 0 8px 24px rgba(198,138,130,0.14)`

#### 3a. いま話題のランキング
- h3: 「🏆 いま話題のランキング」フォント `Zen Maru Gothic 900 / 20px`
- ol (`.rank-list`): items から先頭 5 件を新しい順で表示
- 各 li: 背景 `#fff8f2`、`border: 2px solid #fff`、`border-radius: 16px`、`padding: 12px 14px`
- **rank-num**（円形バッジ 30×30、`Fredoka 700 / 15px`）:
  - 1 位: `linear-gradient(180deg, #ffd970, #ffb84a)`、色 `#7a4a1a`
  - 2 位: `linear-gradient(180deg, #e6e6e6, #b8b8b8)`、色 `#555`
  - 3 位: `linear-gradient(180deg, #ffcda0, #e29a6a)`、色 `#7a4a1a`
  - 4-5 位: `linear-gradient(180deg, #ffd970, #ffb08c)`、色 `#7a4a1a`
- rank-title: `M PLUS Rounded 1c 700 / 13.5px`、2 行で truncate、色 `#4a3630`
- rank-meta: 11px 700、色 `#9c8078`、`"<カテゴリ> · <出典>"`

#### 3b. カテゴリで探す
- h3: 「🎀 カテゴリで探す」
- `.cat-guide`: `grid-template-columns: 1fr 1fr; gap: 10px`
- 各 `.cat-tile` はカテゴリ 1 つに対応、クリックすると `state.active` を切替＋`#board` にスムーズスクロール
- タイル共通: `border: 3px solid <色>`、`border-radius: 18px`、`padding: 14px`、flex 縦積み
- カテゴリ別色:
  | key | ボーダー | 背景 gradient |
  |-----|----------|----------------|
  | goods (t-goods) | `#ffcadd` | `#fff5f9 → #ffe4ee` |
  | collab (t-collab) | `#ffdca8` | `#fff8ea → #ffedcf` |
  | anime (t-anime) | `#c9d8ff` | `#f2f6ff → #dbe6ff` |
  | other (t-other) | `#c5eeda` | `#eefaf3 → #d4f5e8` |
- 内容: `<icn 絵文字 22px>` `<name 800/14px>` `<cnt "N 件のトピック" 700/11px 色 #9c8078>`
- ホバー: `translateY(-2px)` + `box-shadow: 0 6px 0 #ffe1ec`

### 4. Board（最新まとめ）
- セクション id: `board`
- **sec-head**: h2「きょうの最新まとめ」+ サブラベル（動的に「全 N 件・半日おきに自動でおかわりされるよ♡」等）
  - h2: `Zen Maru Gothic 900 / 28px`、前に円形ドット（26×26、`#ff8fb8`、`box-shadow: 0 4px 0 #ff6ea3, inset -4px -4px 0 rgba(255,255,255,0.3)`）
  - sub: 700 / 13px、色 `#9c8078`
- **controls**（カテゴリフィルタ）:
  - ボタン共通: 白背景、`border: 3px solid #fff`、`border-radius: 999px`、`padding: 10px 18px`、`box-shadow: 0 4px 0 #ffe0d0`
  - 内容: `<絵文字> <ラベル> <件数バッジ>`
  - 件数バッジ: `background: #ffe1ec; color: #ff6ea3; padding: 1px 8px; border-radius: 999px; font: 800/11px`
  - active 時: 背景 `linear-gradient(180deg, #ff8fb8 0%, #ff6ea3 100%)`、色 `#fff`、`box-shadow: 0 4px 0 #d94f7e`。件数バッジは白背景＋ピンク文字に反転
  - ホバー: `translateY(-2px)` + 影を 6px に伸ばす
  - 「すべて」の絵文字は 💖。各カテゴリの絵文字は goods=🎀 / collab=🍰 / anime=🎬 / other=🌱
- **board**（カード一覧）:
  - `grid-template-columns: repeat(3, 1fr); gap: 20px`（980px 以下で 2 列、640px 以下で 1 列）
  - 各カード: 白背景、`border: 3px solid #fff`、`border-radius: 24px`、`overflow: hidden`、`box-shadow: 0 6px 0 rgba(255,143,184,0.14), 0 14px 30px rgba(198,138,130,0.12)`
  - ホバー: `translateY(-4px)` + 影を大きく
- **カード上部（thumb）**: 高さ 130px、カテゴリ別の gradient 背景 + `radial-gradient` の白丸ドット装飾
  - goods: `linear-gradient(135deg, #ffd0e0 0%, #ffb8d5 100%)`
  - collab: `linear-gradient(135deg, #ffe4a8 0%, #ffc47a 100%)`
  - anime: `linear-gradient(135deg, #c9d8ff 0%, #a8bfff 100%)`
  - other: `linear-gradient(135deg, #c5eeda 0%, #9be6c8 100%)`
  - 中央にカテゴリ絵文字を `font-size: 54px`、`drop-shadow(0 4px 0 rgba(0,0,0,0.06))` で表示
- **カード本体（card-body）**: `padding: 16px 18px 18px`、flex 縦積み、`gap: 10px`
  - **badge-row**: 左にカテゴリバッジ、右に出典（`nowrap` + `text-overflow: ellipsis`、最大 55%）
    - バッジは `padding: 5px 11px; border-radius: 999px; color: #fff; font: 800/11px`
    - 背景色: goods=`#ff6ea3` / collab=`#e89a3a` / anime=`#6b8dea` / other=`#4bb98a`
    - 出典: 11px 700、色 `#9c8078`
  - **h3**（タイトル）: `Zen Maru Gothic 700 / 15px`、`line-height: 1.5`、3 行で truncate（`-webkit-line-clamp: 3`）
    - タイトル末尾の `" - <配信元>"` は正規表現 `/ - .+$/` で除去して表示
  - **summary**: 12.5px 500、`line-height: 1.75`、2 行 truncate、色 `#9c8078`、末尾 80 文字超は `…`
  - **links**: `justify-content: space-between; align-items: center`
    - 「よんでみる ♡」ボタン: 背景 `#ffe1ec`、色 `#ff6ea3`、`padding: 7px 14px`、`border-radius: 999px`、`font: 800/12px`。ホバーで背景 `#ff8fb8` + 色 `#fff`。`target="_blank"` + `rel="noopener noreferrer"`
    - 日付: 11px 700、色 `#9c8078`（形式は `YYYY-MM-DD HH:mm`）

### 5. Footer
- 白背景、`border: 3px solid #fff`、`border-radius: 32px`、`padding: 26px 28px`、`margin-top: 44px`
- grid `1fr auto`、`gap: 16px`
- 左: 「**ちいかわぽけっと**は、ネット上のちいかわ関連ニュースを自動で集めて、カテゴリ別に見やすくまとめる非公式のファン向けまとめサイトです。」
- 右: 更新バッジ（pill、背景 `#ffe1ec`、色 `#ff6ea3`、`padding: 10px 16px`、`font: 800/12px`、内容「最終更新: YYYY-MM-DD HH:MM JST」）
- 下段（`grid-column: 1 / -1`、上ボーダー `2px dashed #ffe0d0`）:
  - © それぞれの記事の著作権は各配信元に帰属します。当サイトは記事本文を転載せず、見出し・短い要約・出典リンクのみを掲載しています。「ちいかわ」および関連キャラクターの権利は原作者・ナガノ先生および関係各社に帰属します。当サイトは非公式・ファン運営です。

## Interactions & Behavior

### カテゴリフィルタ
- 上部の Controls ボタン、または「カテゴリで探す」タイルをクリックすると、`state.active` を切替
- `state.active === 'all'` のときは全件、それ以外は `items.filter(item => item.category_key === state.active)`
- カテゴリタイルをクリックした場合は、追加で `#board` にスムーズスクロール（`scrollIntoView({ behavior: 'smooth', block: 'start' })`）
- アクティブなボタンは `.active` クラス（背景ピンクグラデ）
- sub ラベルはフィルタに応じて動的に書き換え

### アニメーション
- ハート `♡` の鼓動: `@keyframes hb` で 1.4s ease-in-out infinite、`transform: scale(1) → scale(1.18) → scale(1)`
- カード / タイル / ボタンのホバー: `transform: translateY(-2px 〜 -4px)` + 影拡大、`transition: .15s 〜 .2s`
- `prefers-reduced-motion: reduce` を尊重（すべてのアニメと transition を無効化）

### レスポンシブ
- **≤ 980px**: Hero を 1 カラムに、右ビジュアル最大 260px、Side Row を 1 カラム、Board を 2 カラム、ナビメニューを非表示、Footer を 1 カラム
- **≤ 640px**: shell padding を縮小、Hero を `24px 20px + border-radius 28px`、h1 32px、Board を 1 カラム、m-chip を小さく

### 状態が空のとき
- 該当カテゴリに記事なし → 「このカテゴリはまだ準備中…／次のおかわりを待っててね♡」を 1 枚のカードとして表示
- データ読み込み失敗 → 「データを読み込めなかったよ…／また来てね♡」

## State Management
- **state.active**: 現在のフィルタキー（`"all" | "goods" | "collab" | "anime" | "other"`）。初期値 `"all"`
- **state.items**: 記事オブジェクトの配列（下記 Data Schema）
- **state.categories**: カテゴリ定義の配列
- **state.meta**: メタ情報（生成時刻、更新間隔、情報源）

Vue / React 化する場合、上記は 1 コンポーネントの局所状態で十分（グローバルストア不要）。

## Data Schema
`items.json` は以下の形。ビルド時にバッチで生成し、静的にバンドルする想定。

```json
{
  "site_title": "ちいかわぽけっと",
  "query": "ちいかわ",
  "generated_at": "2026-09-13T17:39:17.049680+09:00",
  "generated_at_jst": "2026-09-13 17:39 JST",
  "update_interval_hours": 12,
  "sources": [
    { "name": "Google ニュース 検索RSS", "url": "https://news.google.com/rss/search?q=..." }
  ],
  "categories": [
    { "key": "goods",  "label": "グッズ",       "count": 5, "icon": "🎀", "desc": "..." },
    { "key": "collab", "label": "コラボ",       "count": 2, "icon": "🍰", "desc": "..." },
    { "key": "anime",  "label": "アニメ・映画", "count": 2, "icon": "🎬", "desc": "..." },
    { "key": "other",  "label": "そのほか",     "count": 3, "icon": "🌱", "desc": "..." }
  ],
  "items": [
    {
      "title": "...",
      "link": "https://news.google.com/rss/articles/...",
      "source": "NEWSポストセブン",
      "snippet": "...",
      "summary": "...",
      "category_key": "collab",
      "category_label": "コラボ",
      "published_at": "2026-09-13T16:00:00+09:00",
      "published_display": "2026-09-13 16:00"
    }
  ]
}
```

### バックエンド（バッチ）に関する補足
- **収集**: Google ニュース検索 RSS を起点に、URL の `q=` を「ちいかわ」（URL エンコード済）にしたエンドポイントを 12 時間ごとに fetch
- **カテゴリ判定**: タイトル文字列にキーワードを含むかで単純分類
  - goods: 「グッズ」「マスコット」「ぬい」「プライズ」「アイテム」「発売」「バッグ」「パン」「ベーカリー」
  - collab: 「コラボ」「くら寿司」「カフェ」「タイアップ」「限定」
  - anime: 「映画」「アニメ」「劇場」「配信」「興行」
  - other: 上記いずれも該当しない場合
- **重複除去**: 同一 link は除外、タイトルの正規化文字列（記号除去＋前後 20 文字）で近似重複も除外
- **要約**: 元記事本文は取得せず、RSS の `description` を最大 100〜120 文字にトリム

## Design Tokens

### Colors
```
--bg-1:          #fff4ea   /* ベース背景（クリーム） */
--bg-2:          #ffe6f1   /* 背景 pink 域 */
--bg-3:          #e8f6ff   /* 背景 sky 域 */
--paper:         #ffffff   /* カード / パネル */
--ink:           #4a3630   /* メイン文字 */
--ink-soft:      #6b4f47   /* サブ文字 */
--muted:         #9c8078   /* 補助テキスト */
--line:          #ffe0d0   /* 罫線 / 影の受け色 */

--pink:          #ff8fb8   /* アクセント */
--pink-deep:     #ff6ea3   /* アクセント濃 */
--pink-soft:     #ffe1ec

--yellow:        #ffd970
--yellow-soft:   #fff2c4

--mint:          #9be6c8
--mint-soft:     #d4f5e8

--sky:           #8ecbff
--sky-soft:      #dcefff

--lav:           #c5b0ff
--lav-soft:      #ece2ff

--peach:         #ffb08c
```

背景全体は 4 つの `radial-gradient` を `linear-gradient(180deg, #fff4ea 0%, #ffeaf3 55%, #fff7de 100%)` に重ねる。加えて `body::before` に固定位置で白い小さな水玉模様を敷く（詳細は CSS 参照）。

### Typography
- 本文: `"M PLUS Rounded 1c", "Hiragino Maru Gothic ProN", "Yu Gothic", sans-serif`
- 見出し: `"Zen Maru Gothic", sans-serif`
- 数字の強調: `"Fredoka", "Zen Maru Gothic", sans-serif`
- Google Fonts 読み込み: `M+PLUS+Rounded+1c:wght@400;500;700;800;900`、`Zen+Maru+Gothic:wght@500;700;900`、`Fredoka:wght@600;700`

サイズ／太さのおおまかな階層：
| 用途 | フォント / 太さ / サイズ |
|------|--------------------------|
| H1 (Hero) | Zen Maru Gothic 900 / `clamp(36px, 5.4vw, 62px)` |
| H2 (セクション) | Zen Maru Gothic 900 / 28px |
| H3 (Box) | Zen Maru Gothic 900 / 20px |
| カードタイトル | Zen Maru Gothic 700 / 15px |
| 本文 lead | M PLUS Rounded 1c 500 / 15.5px |
| 本文 (要約) | M PLUS Rounded 1c 500 / 12.5px |
| メトリクス数字 | Fredoka 700 / 26px |
| バッジ / ラベル | M PLUS Rounded 1c 800 / 11〜13px |

### Spacing scale
`20px / 22px / 24px / 26px / 28px / 40px / 44px` を主に使用。カード内 gap は `10px / 12px / 14px`。

### Border radius
- ボタン / ピル: `999px`
- 小カード / チップ: `16px 〜 18px`
- 標準カード: `24px`
- 大パネル / Footer: `32px`
- Hero: `40px`（≤640px で 28px）

### Shadows
- ソフトシャドウ: `0 8px 24px rgba(198,138,130,0.14)`
- カード基本: `0 6px 0 rgba(255,143,184,0.14), 0 14px 30px rgba(198,138,130,0.12)`
- Hero: `0 10px 0 rgba(255,143,184,0.18), 0 20px 40px rgba(255,143,184,0.15)`
- ボタン 3D 押し感: `0 4px 0 <受け色>`（ホバーで `0 6px 0 <受け色>` へ）

## Assets

このデザインでは**バイナリ画像を使用していません**。以下はすべて絵文字またはユニコード記号、または CSS 描画です：

- ロゴマーク / メインビジュアルのキャラ / 雲 / 耳・目・ほっぺ・口 → すべて CSS で描画（HTML 内の `.logo-mark` `.mv-cloud` `.mv-face` を参照）
- キラキラ: `✧` `✦`（テキスト）
- カテゴリアイコン: `🎀 🍰 🎬 🌱`
- ランキング見出しの `🏆`、カテゴリガイド見出しの `🎀`、フィルタ「すべて」の `💖`、ハート `♡`

将来的に公式素材や自前イラストに差し替える場合は、CSS 描画部を `<img>` に置き換えれば OK です（サイズと角丸は `.logo-mark`（40×40 / 円形）、`.mv-face`（正方形コンテナ内 44%）を踏襲）。

## Files
このバンドルに含まれるファイル：
- `chiikawa-fansite.html` — 単一ファイルで完結する高忠実モック。実データ入りの `<script type="application/json" id="embedded-data">` と、フィルタ／レンダリング用の素の JavaScript を含む。

エンジニアはこの HTML を参照しながら、ターゲット環境で以下を再実装してください：
1. 上記の Design Tokens をアプリの CSS 変数 / Tailwind config に反映
2. セクションごとにコンポーネント化（`<Navbar/>` `<Hero/>` `<SideRow/>` `<Board/>` `<Footer/>`）
3. `items.json` をビルド時に読み込み、`Board` と `Ranking` に流し込み
4. `<style>` 内の keyframes とレスポンシブブレイクポイントを踏襲
5. `prefers-reduced-motion` の respect を維持

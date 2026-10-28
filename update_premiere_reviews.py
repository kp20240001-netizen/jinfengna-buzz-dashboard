#!/usr/bin/env python3
"""
《消失的金鳳娜》10/29 上映日「首映 24 小時口碑」本機零 Token 靜態快照生成器
讀取 /workspace/jinfengna_dashboard/premiere_reviews_data.json，
一鍵生成：
1. /workspace/jinfengna_dashboard/premiere_24h_reviews.html
2. /workspace/jinfengna_dashboard/static_site/premiere_24h_reviews.html
3. /workspace/jinfengna_dashboard/docs/premiere_24h_reviews.html
並於戰情室首頁 (/workspace/jinfengna_dashboard/docs/index.html) 嵌入首映 24h 口碑快照專區與一鍵導流入口。
"""
import datetime
import json
import os
import shutil

BASE_DIR = "/workspace/jinfengna_dashboard"
DATA_JSON = os.path.join(BASE_DIR, "premiere_reviews_data.json")
OUT_MAIN = os.path.join(BASE_DIR, "premiere_24h_reviews.html")
STATIC_DIR = os.path.join(BASE_DIR, "static_site")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

TZ_TAIPEI = datetime.timezone(datetime.timedelta(hours=8))

FORBIDDEN_REDLINE = "死亡" + "賭局"


def verify_redline(text: str):
    if FORBIDDEN_REDLINE in text:
        raise ValueError("RED LINE VIOLATION: Forbidden 4-character phrase detected!")


def build_html(data: dict) -> str:
    now_str = datetime.datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M (台北時間 UTC+8)")
    hs = data["hero_stats"]

    critic_cards = []
    for c in data["critic_and_celebrity_quotes"]:
        critic_cards.append(f"""
        <article class="critic-card">
          <div class="critic-top">
            <span class="critic-tag">{c['tag']}</span>
            <span class="critic-stars">{c['rating']}</span>
          </div>
          <blockquote class="critic-quote">{c['quote']}</blockquote>
          <div class="critic-footer">
            <span class="critic-author">— {c['author']}</span>
            <span class="critic-source">{c['source_platform']}</span>
          </div>
        </article>
        """)

    audience_cards = []
    for a in data["audience_24h_wall"]:
        audience_cards.append(f"""
        <div class="aud-card">
          <div class="aud-header">
            <div>
              <strong class="aud-handle">{a['handle']}</strong>
              <span class="aud-pf">{a['platform']}</span>
            </div>
            <span class="aud-sentiment">{a['sentiment']}</span>
          </div>
          <p class="aud-body">{a['comment']}</p>
          <div class="aud-meta">
            <span>🕒 {a['time_badge']}</span>
            <span class="aud-likes">❤️ +{a['likes']} 讚</span>
          </div>
        </div>
        """)

    theater_rows = []
    for t in data["theaters_and_ticketing"]:
        theater_rows.append(f"""
        <tr>
          <td class="td-region">{t['region']}</td>
          <td class="td-theaters">{t['theaters']}</td>
          <td class="td-note">{t['sessions_note']}</td>
          <td class="td-action">
            <a href="{t['booking_url']}" target="_blank" rel="noopener" class="ticket-btn">🎟️ 場次查詢／訂票</a>
          </td>
        </tr>
        """)

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{data['movie_title']}｜10/29 首映 24 小時零負評口碑牆 ＆ 全台戲院場次導流</title>
  <style>
    :root {{
      --bg-dark: #0b0d13;
      --bg-card: #141824;
      --bg-card-alt: #1b2030;
      --gold: #f5c451;
      --gold-soft: #fae094;
      --crimson: #d94b43;
      --text-main: #f3f5f9;
      --text-muted: #9aa4b8;
      --border-gold: rgba(245, 196, 81, 0.28);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
      background: radial-gradient(circle at 50% 0%, #1c2236 0%, #0b0d13 65%);
      color: var(--text-main);
      line-height: 1.65;
      padding-bottom: 64px;
    }}
    .top-bar {{
      background: rgba(11, 13, 19, 0.92);
      border-bottom: 1px solid var(--border-gold);
      padding: 14px 24px;
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      backdrop-filter: blur(10px);
    }}
    .top-bar-brand {{
      font-weight: 800;
      font-size: 1.05rem;
      color: var(--gold);
      letter-spacing: 0.04em;
    }}
    .top-bar-links a {{
      color: var(--text-main);
      text-decoration: none;
      font-size: 0.9rem;
      padding: 6px 14px;
      border-radius: 999px;
      border: 1px solid var(--border-gold);
      margin-left: 8px;
      transition: all 0.2s;
    }}
    .top-bar-links a:hover {{
      background: var(--gold);
      color: #0b0d13;
      font-weight: 700;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
    }}
    .hero {{
      padding: 48px 0 36px;
      text-align: center;
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }}
    .zero-token-pill {{
      display: inline-block;
      background: rgba(46, 204, 113, 0.15);
      border: 1px solid rgba(46, 204, 113, 0.5);
      color: #6ee7b7;
      font-size: 0.82rem;
      font-weight: 700;
      padding: 5px 16px;
      border-radius: 999px;
      margin-bottom: 16px;
    }}
    .hero h1 {{
      font-size: clamp(1.85rem, 4vw, 2.75rem);
      font-weight: 900;
      color: #ffffff;
      letter-spacing: 0.04em;
      margin-bottom: 12px;
    }}
    .hero h1 span {{
      color: var(--gold);
    }}
    .hero-sub {{
      color: var(--text-muted);
      font-size: 1.05rem;
      max-width: 780px;
      margin: 0 auto 28px;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-top: 24px;
    }}
    .kpi-card {{
      background: linear-gradient(160deg, #191f30 0%, #121622 100%);
      border: 1px solid var(--border-gold);
      border-radius: 14px;
      padding: 20px;
      text-align: center;
      box-shadow: 0 10px 30px rgba(0,0,0,0.45);
    }}
    .kpi-val {{
      font-size: 1.75rem;
      font-weight: 900;
      color: var(--gold);
      margin-bottom: 4px;
    }}
    .kpi-lbl {{
      font-size: 0.9rem;
      color: var(--text-muted);
    }}
    .section-title {{
      margin: 44px 0 20px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 10px;
      border-left: 4px solid var(--gold);
      padding-left: 14px;
    }}
    .section-title h2 {{
      font-size: 1.45rem;
      font-weight: 800;
      color: #fff;
    }}
    .section-title span {{
      font-size: 0.88rem;
      color: var(--text-muted);
    }}
    .critic-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
      gap: 20px;
    }}
    .critic-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-gold);
      border-radius: 14px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .critic-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }}
    .critic-tag {{
      background: rgba(245, 196, 81, 0.16);
      color: var(--gold);
      font-size: 0.78rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
    }}
    .critic-stars {{
      color: var(--gold);
      letter-spacing: 2px;
      font-size: 0.95rem;
    }}
    .critic-quote {{
      font-size: 1.02rem;
      font-weight: 600;
      color: #f8fafc;
      margin-bottom: 18px;
      line-height: 1.7;
    }}
    .critic-footer {{
      border-top: 1px solid rgba(255,255,255,0.08);
      padding-top: 12px;
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      color: var(--text-muted);
    }}
    .aud-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 18px;
    }}
    .aud-card {{
      background: var(--bg-card-alt);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 12px;
      padding: 20px;
    }}
    .aud-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}
    .aud-handle {{
      color: var(--gold-soft);
      font-size: 0.95rem;
      margin-right: 8px;
    }}
    .aud-pf {{
      background: rgba(255,255,255,0.1);
      color: #cbd5e1;
      font-size: 0.75rem;
      padding: 2px 8px;
      border-radius: 4px;
    }}
    .aud-sentiment {{
      font-size: 0.8rem;
      font-weight: 700;
      color: #fca5a5;
    }}
    .aud-body {{
      font-size: 0.95rem;
      color: #e2e8f0;
      margin-bottom: 14px;
    }}
    .aud-meta {{
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    .aud-likes {{
      color: var(--gold);
      font-weight: 700;
    }}
    .table-wrap {{
      background: var(--bg-card);
      border: 1px solid var(--border-gold);
      border-radius: 14px;
      overflow-x: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 680px;
    }}
    th, td {{
      padding: 16px 18px;
      text-align: left;
      border-bottom: 1px solid rgba(255,255,255,0.07);
    }}
    th {{
      background: rgba(245, 196, 81, 0.1);
      color: var(--gold);
      font-size: 0.88rem;
      font-weight: 800;
    }}
    .td-region {{
      font-weight: 800;
      color: var(--gold-soft);
      white-space: nowrap;
    }}
    .td-theaters {{
      font-size: 0.92rem;
      color: #f1f5f9;
    }}
    .td-note {{
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
    .ticket-btn {{
      display: inline-block;
      background: linear-gradient(135deg, #f5c451 0%, #d99b26 100%);
      color: #0b0d13;
      font-weight: 800;
      font-size: 0.85rem;
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 8px;
      white-space: nowrap;
    }}
    .footer-note {{
      margin-top: 40px;
      text-align: center;
      font-size: 0.84rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>
  <nav class="top-bar">
    <div class="top-bar-brand">🎬 {data['movie_title']}｜10/29 首映 24 小時口碑靜態快照牆</div>
    <div class="top-bar-links">
      <a href="index.html">⬅ 返回即時聲量戰情室主頁</a>
      <a href="#theaters">🎟️ 全台上映戲院與訂票導流</a>
    </div>
  </nav>

  <main class="container">
    <section class="hero">
      <div class="zero-token-pill">⚡ {data['snapshot_mode']}｜更新時間：{now_str}</div>
      <h1>{data['movie_title']}<br /><span>10/29 首映 24 小時觀眾與影評零負評口碑牆</span></h1>
      <p class="hero-sub">
        高雄電影節世界首映滿場完售、金馬聯名特映與全台試片場一致盛讚！以下彙整首波影評人權威背書、Threads / IG / PTT / Dcard 觀眾真實映後眼淚回饋，以及 10/29（週四）全台上映戲院場次導流。
      </p>
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-val">{hs['satisfaction_rate']}</div>
          <div class="kpi-lbl">首波特映觀眾滿意度</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val">{hs['critic_consensus']}</div>
          <div class="kpi-lbl">影評與媒體試片口碑</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val">{hs['threads_ig_mentions']}</div>
          <div class="kpi-lbl">社群自發映後推薦串</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val">{hs['kff_premiere_status']}</div>
          <div class="kpi-lbl">影展首映指標表現</div>
        </div>
      </div>
    </section>

    <section id="critics">
      <div class="section-title">
        <h2>🏆 影展選片人、資深影評與媒體首映金句牆</h2>
        <span>100% 實名特映與影展權威背書</span>
      </div>
      <div class="critic-grid">
        {"".join(critic_cards)}
      </div>
    </section>

    <section id="audience">
      <div class="section-title">
        <h2>💬 首映 24 小時觀眾真實映後回饋（Threads / IG / PTT / Dcard）</h2>
        <span>本機 update_premiere_reviews.py 零 Token 靜態渲染</span>
      </div>
      <div class="aud-grid">
        {"".join(audience_cards)}
      </div>
    </section>

    <section id="theaters">
      <div class="section-title">
        <h2>🎟️ 10/29（週四）全台上映戲院與場次訂票導流</h2>
        <span>支援文化幣折抵、團體包場與交換券劃位</span>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>上映地區</th>
              <th>首波聯映戲院清單</th>
              <th>場次與購票資訊</th>
              <th>快速訂票導流</th>
            </tr>
          </thead>
          <tbody>
            {"".join(theater_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <p class="footer-note">
      本頁面由 <code>/workspace/jinfengna_dashboard/update_premiere_reviews.py</code> 讀取 <code>premiere_reviews_data.json</code> 自動生成（0 Grok Token 消耗）。
    </p>
  </main>
</body>
</html>
"""
    verify_redline(html)
    return html


def main():
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)

    with open(DATA_JSON, "r", encoding="utf-8") as f:
        raw_text = f.read()
    verify_redline(raw_text)
    data = json.loads(raw_text)

    html = build_html(data)

    for target in [
        OUT_MAIN,
        os.path.join(STATIC_DIR, "premiere_24h_reviews.html"),
        os.path.join(DOCS_DIR, "premiere_24h_reviews.html"),
    ]:
        with open(target, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] Wrote {target} ({len(html)} bytes)")

    # Also copy docs/index.html into static_site/index.html and inject banner link if not present
    docs_index = os.path.join(DOCS_DIR, "index.html")
    if os.path.exists(docs_index):
        with open(docs_index, "r", encoding="utf-8") as f:
            idx_html = f.read()
        banner_snippet = (
            '<div style="background:linear-gradient(90deg,#1b2030,#2a2112);border:1px solid #f5c451;'
            'padding:12px 20px;border-radius:10px;margin:14px auto;max-width:1200px;display:flex;'
            'justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">'
            '<span style="color:#f5c451;font-weight:800;">🔥 10/29 上映日備戰專區：首映 24 小時觀眾與影評零負評口碑牆（0-Token 靜態快照）已上線！</span>'
            '<a href="premiere_24h_reviews.html" style="background:#f5c451;color:#0b0d13;font-weight:800;'
            'padding:6px 16px;border-radius:6px;text-decoration:none;">👉 開啟首映 24h 口碑快照頁</a></div>'
        )
        if "premiere_24h_reviews.html" not in idx_html and "<main" in idx_html:
            idx_html = idx_html.replace("<main", banner_snippet + "\n<main", 1)
            verify_redline(idx_html)
            with open(docs_index, "w", encoding="utf-8") as f:
                f.write(idx_html)
        shutil.copy2(docs_index, os.path.join(STATIC_DIR, "index.html"))


if __name__ == "__main__":
    main()

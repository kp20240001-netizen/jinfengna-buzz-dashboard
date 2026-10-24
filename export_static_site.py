# -*- coding: utf-8 -*-
import json
import os
import pandas as pd

BASE_DIR = "/workspace/jinfengna_dashboard"
with open(os.path.join(BASE_DIR, "dashboard_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

os.makedirs(os.path.join(BASE_DIR, "docs"), exist_ok=True)

# Build Heatmap Rows
hm_rows_html = []
hm_platforms = []
for r in data["heatmap_rows"]:
    pf = r["平台"]
    if pf not in hm_platforms:
        hm_platforms.append(pf)
    st_label = r["狀態燈號"]
    if "🟢" in st_label:
        status_code = "green"
        today_cls = "cell-today-green"
        badge_html = "<span class='status-pill status-pill-green'>🟢 成長</span>"
    elif "🟡" in st_label:
        status_code = "yellow"
        today_cls = "cell-today-yellow"
        badge_html = "<span class='status-pill status-pill-yellow'>🟡 持平</span>"
    else:
        status_code = "red"
        today_cls = "cell-today-red"
        badge_html = "<span class='status-pill status-pill-red'>🔴 下滑</span>"

    # Extract delta string from 關鍵數字與判讀
    insight = r["關鍵數字與判讀"]
    hm_rows_html.append(
        f"<tr class='hm-row' data-status='{status_code}' data-pf='{pf}'>"
        f"<td><span class='pf-tag'>{pf}</span></td>"
        f"<td class='col-metric'>{r['核心指標']}</td>"
        f"<td class='col-num col-val'>{r.get('10/15', '—')}</td>"
        f"<td class='col-num col-val'>{r.get('10/22 首映', '—')}</td>"
        f"<td class='col-num col-val'>{r.get('10/23', '—')}</td>"
        f"<td class='col-num col-val {today_cls}'>{r.get('10/24 今日', '—')}</td>"
        f"<td class='col-center'>{badge_html}</td>"
        f"<td class='col-delta'>{insight}</td>"
        f"</tr>"
    )

# Build Granular Quantitative Rows
quant_rows_html = []
for r in data["quantitative_full_table"]:
    pf = r["平台"]
    if "YouTube" in pf:
        cat_group = "YouTube"
    elif "Facebook" in pf:
        cat_group = "Facebook"
    elif "Instagram" in pf:
        cat_group = "Instagram"
    elif "Threads" in pf:
        cat_group = "Threads"
    elif "Dcard" in pf or "PTT" in pf:
        cat_group = "Dcard / PTT"
    elif "新聞" in pf:
        cat_group = "新聞媒體"
    else:
        cat_group = "Google Trends / X"

    st_val = r["狀態"]
    if "🟢" in st_val:
        st_badge = "<span class='status-pill status-pill-green'>🟢 成長</span>"
    elif "🟡" in st_val:
        st_badge = "<span class='status-pill status-pill-yellow'>🟡 持平</span>"
    else:
        st_badge = "<span class='status-pill status-pill-red'>🔴 下滑</span>"

    search_text = f"{pf} {r['指標名稱']} {r.get('2026-10-24','')} {r['單日變化']}".lower()
    quant_rows_html.append(
        f"<tr class='detail-item' data-group='{cat_group}' data-search='{search_text}'>"
        f"<td><span class='pf-tag'>{pf}</span></td>"
        f"<td class='col-metric'>{r['指標名稱']}</td>"
        f"<td class='col-num'>{r.get('09/17–10/15', '—')}</td>"
        f"<td class='col-num'>{r.get('2026-10-22', '—')}</td>"
        f"<td class='col-num'>{r.get('2026-10-23', '—')}</td>"
        f"<td class='col-num col-highlight'>{r.get('2026-10-24', '—')}</td>"
        f"<td class='col-num col-delta-text'>{r['單日變化']}</td>"
        f"<td class='col-center'>{st_badge}</td>"
        f"</tr>"
    )

# Build YouTube Comments Rows
ytc_rows_html = []
for c in data["youtube_comments_12"]:
    s_txt = f"youtube {c['所屬影片']} {c['留言者']} {c['留言內容']} {c['情緒與話題分類']}".lower()
    ytc_rows_html.append(
        f"<tr class='detail-item' data-group='YouTube' data-search='{s_txt}'>"
        f"<td class='col-center'>{c['編號']}</td>"
        f"<td><span class='pf-tag'>{c['所屬影片']}</span></td>"
        f"<td class='col-author'>{c['留言者']}</td>"
        f"<td><a href='{c['連結']}' target='_blank' rel='noopener' class='comment-link'>{c['留言內容']}</a></td>"
        f"<td class='col-num col-delta-text'>+{c['按讚數']} 讚</td>"
        f"<td><span class='chip-tag'>{c['情緒與話題分類']}</span></td>"
        f"</tr>"
    )

# Build PTT Rows
ptt_rows_html = []
for idx, p in enumerate(data["ptt_pushes_15"], 1):
    s_txt = f"ptt {p['文章']} {p['作者']} {p['內容']}".lower()
    t_cls = "status-pill-green" if p["推文類型"] == "推" else ("status-pill-red" if p["推文類型"] == "噓" else "status-pill-yellow")
    ptt_rows_html.append(
        f"<tr class='detail-item' data-group='Dcard / PTT' data-search='{s_txt}'>"
        f"<td class='col-center'>{idx}</td>"
        f"<td><span class='pf-tag'>{p['文章']}</span></td>"
        f"<td class='col-center'><span class='status-pill {t_cls}'>{p['推文類型']}</span></td>"
        f"<td class='col-author'>{p['作者']}</td>"
        f"<td>{p['內容']}</td>"
        f"</tr>"
    )

# Build News Rows
news_rows_html = []
for idx, n in enumerate(data["extra_news_7"], 1):
    s_txt = f"新聞媒體 {n['日期']} {n['媒體']} {n['標題']}".lower()
    news_rows_html.append(
        f"<tr class='detail-item' data-group='新聞媒體' data-search='{s_txt}'>"
        f"<td class='col-center'>{idx}</td>"
        f"<td class='col-num'>{n['日期']}</td>"
        f"<td><span class='pf-tag'>{n['媒體']}</span></td>"
        f"<td class='col-metric'>{n['標題']}</td>"
        f"<td><a href='{n['連結']}' target='_blank' rel='noopener' class='action-link'>閱讀原文 ↗</a></td>"
        f"</tr>"
    )

# Dcard info
dc = data["dcard_details"]
tag = dc["topic_tag"]

# Prepare Chart JSON Data
chart_payload = {
    "trends_daily": data["trends_daily"],
    "total_buzz_trend": data["total_buzz_trend"],
    "pie_views": data["pie_views"],
    "pie_engagement": data["pie_engagement"],
    "yt_comments": data["youtube_comments_12"],
    "quant_csv": data["quantitative_full_table"]
}
chart_json_str = json.dumps(chart_payload, ensure_ascii=False)

# Write external chart & interaction JS to keep index.html clean and modular
js_code = f"""window.DASHBOARD_DATA = {chart_json_str};

const SNAPSHOTS = {{
  "2026-10-24": {{
    badge: "2026-10-24 最新快照 (UTC+8)",
    heroTotal: "481,648",
    heroDelta: "🟢 +71,298 (+17.4%)",
    heroSub: "核心預告與社群擴散總聲量 264,347（單日 +62,252 / +30.8%），加計新聞媒體與外部長短影音跨平台總觸及達 481,648 次。",
    kpis: [
      {{ val: "198,208", delta: "🟢 +53,751 (+37.2%)", pct: "84%" }},
      {{ val: "1,116 人", delta: "🟢 +350 人 (+45.7%)", pct: "78%" }},
      {{ val: "374 粉 / 757 互動", delta: "🟢 +38 粉 (+11.3%)", pct: "72%" }},
      {{ val: "31.0K 瀏覽 / 1,503 互動", delta: "🟢 單篇最高 980 讚", pct: "88%" }},
      {{ val: "160 則 / 15 推", delta: "🟢 黃金交叉 48 : 18", pct: "80%" }}
    ]
  }},
  "2026-10-23": {{
    badge: "2026-10-23 發酵日歷史快照",
    heroTotal: "410,350",
    heroDelta: "🟢 +68,150 (+19.9%)",
    heroSub: "2026-10-23 發酵日盤點：核心預告與社群總聲量 202,095，A-Lin【寶貝愛人】主題曲 Teaser 首日上架，Threads 自然討論開始發酵。",
    kpis: [
      {{ val: "144,457", delta: "🟢 +29,457 (+25.6%)", pct: "68%" }},
      {{ val: "766 人", delta: "🟢 +210 人 (+37.7%)", pct: "56%" }},
      {{ val: "336 粉 / 610 互動", delta: "🟢 +24 粉 (+7.7%)", pct: "60%" }},
      {{ val: "30.6K 瀏覽 / 820 互動", delta: "🟢 熱門串文發酵中", pct: "65%" }},
      {{ val: "159 則 / 12 推", delta: "🟢 雙片對照 50 : 15", pct: "75%" }}
    ]
  }},
  "2026-10-22": {{
    badge: "2026-10-22 首映日歷史快照",
    heroTotal: "342,200",
    heroDelta: "🟢 +112,400 (+48.9%)",
    heroSub: "2026-10-22 首映會當日：Google Trends 單獨搜尋熱度直衝 100 滿分峰值，雙片對照 50 : 20 正式黃金交叉反超《消失的她》。",
    kpis: [
      {{ val: "115,000", delta: "🟢 +50,000 (+76.9%)", pct: "54%" }},
      {{ val: "556 人", delta: "🟢 首映會派對曝光", pct: "42%" }},
      {{ val: "312 粉 / 480 互動", delta: "🟢 首映造型釋出", pct: "48%" }},
      {{ val: "23.0K 瀏覽 / 420 互動", delta: "🟢 投資方日記開箱", pct: "50%" }},
      {{ val: "153 則 / 9 推", delta: "🟢 首映衝上 100 峰值", pct: "70%" }}
    ]
  }}
}};

function switchSnapshot(dateKey, btn) {{
  document.querySelectorAll('.snap-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  const snap = SNAPSHOTS[dateKey];
  if (!snap) return;
  document.getElementById('hero-snap-badge').textContent = snap.badge;
  document.getElementById('hero-total-val').textContent = snap.heroTotal;
  document.getElementById('hero-total-delta').textContent = snap.heroDelta;
  document.getElementById('hero-sub-text').textContent = snap.heroSub;
  snap.kpis.forEach((k, idx) => {{
    const vEl = document.getElementById('kpi-val-' + idx);
    const dEl = document.getElementById('kpi-delta-' + idx);
    const pEl = document.getElementById('kpi-bar-' + idx);
    if (vEl) vEl.textContent = k.val;
    if (dEl) dEl.textContent = k.delta;
    if (pEl) pEl.style.width = k.pct;
  }});
}}

function setHeatmapViewMode(mode, btn) {{
  document.querySelectorAll('.hm-mode-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  const table = document.getElementById('heatmap-table');
  table.classList.remove('mode-combined', 'mode-values', 'mode-deltas');
  table.classList.add('mode-' + mode);
}}

let currentHmStatus = 'all';
let currentHmPf = 'all';

function filterHeatmapStatus(status, btn) {{
  currentHmStatus = status;
  document.querySelectorAll('.hm-status-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  applyHeatmapFilters();
}}

function filterHeatmapPlatform(pf, btn) {{
  currentHmPf = pf;
  document.querySelectorAll('.hm-pf-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  applyHeatmapFilters();
}}

function applyHeatmapFilters() {{
  document.querySelectorAll('.hm-row').forEach(row => {{
    const stMatch = (currentHmStatus === 'all' || row.getAttribute('data-status') === currentHmStatus);
    const pfMatch = (currentHmPf === 'all' || row.getAttribute('data-pf') === currentHmPf);
    row.style.display = (stMatch && pfMatch) ? '' : 'none';
  }});
}}

let currentDetailGroup = 'ALL';
function filterDetailsGroup(group, btn) {{
  currentDetailGroup = group;
  document.querySelectorAll('.detail-pf-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  applyDetailsSearch();
}}

function applyDetailsSearch() {{
  const q = (document.getElementById('detail-search-input').value || '').trim().toLowerCase();
  document.querySelectorAll('.detail-item').forEach(row => {{
    const g = row.getAttribute('data-group') || '';
    const s = row.getAttribute('data-search') || '';
    const gMatch = (currentDetailGroup === 'ALL' || g === currentDetailGroup);
    const qMatch = (!q || s.includes(q));
    row.style.display = (gMatch && qMatch) ? '' : 'none';
  }});
}}

function switchDetailTab(tabId, btn) {{
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  document.querySelectorAll('.detail-tab-pane').forEach(p => p.classList.remove('active'));
  const target = document.getElementById(tabId);
  if (target) target.classList.add('active');
}}

function exportCSV() {{
  const rows = window.DASHBOARD_DATA.quant_csv || [];
  if (!rows.length) return;
  const headers = Object.keys(rows[0]);
  const csvLines = [
    headers.join(','),
    ...rows.map(r => headers.map(h => '"' + String(r[h] || '').replace(/"/g, '""') + '"').join(','))
  ];
  const blob = new Blob(["\\uFEFF" + csvLines.join('\\n')], {{ type: 'text/csv;charset=utf-8;' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'jinfengna_buzz_metrics_20261024.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}}

function renderCharts() {{
  if (typeof Plotly === 'undefined') return;
  const d = window.DASHBOARD_DATA;
  const fontCfg = {{ family: "'Noto Sans TC', 'Fira Code', sans-serif", size: 12, color: "#E2E8F0" }};
  const gridColor = "rgba(255,255,255,0.07)";
  const paperBg = "rgba(0,0,0,0)";
  const plotBg = "rgba(0,0,0,0)";
  const cfg = {{ responsive: true, displayModeBar: false }};

  // Chart 1: Multi-day Growth Trend
  const tb = d.total_buzz_trend;
  const traceTotal = {{
    x: ["10/15 預告", "10/22 首映日", "10/23 發酵日", "10/24 爆發日"],
    y: tb.total_buzz,
    mode: "lines+markers+text",
    name: "核心聲量總計",
    fill: "tozeroy",
    fillcolor: "rgba(16, 185, 129, 0.13)",
    line: {{ color: "#10B981", width: 3.5, shape: "spline" }},
    marker: {{ size: 9, color: "#10B981" }},
    text: tb.total_buzz.map(v => v.toLocaleString()),
    textposition: "top center",
    textfont: {{ family: "'Fira Code', monospace", size: 11, color: "#6EE7B7" }}
  }};
  const traceYT = {{
    x: ["10/15 預告", "10/22 首映日", "10/23 發酵日", "10/24 爆發日"],
    y: tb.yt_long,
    mode: "lines+markers",
    name: "YouTube 長片觀看",
    line: {{ color: "#38BDF8", width: 2.5, dash: "dash", shape: "spline" }},
    marker: {{ size: 7, color: "#38BDF8" }}
  }};
  const traceSocial = {{
    x: ["10/15 預告", "10/22 首映日", "10/23 發酵日", "10/24 爆發日"],
    y: tb.social_views_and_eng,
    mode: "lines+markers",
    name: "Threads 瀏覽與社群互動",
    line: {{ color: "#F59E0B", width: 2.5, shape: "spline" }},
    marker: {{ size: 7, color: "#F59E0B" }}
  }};
  Plotly.newPlot("chart-trend-line", [traceTotal, traceYT, traceSocial], {{
    paper_bgcolor: paperBg, plot_bgcolor: plotBg, font: fontCfg,
    height: 340, hovermode: "x unified",
    margin: {{ l: 48, r: 20, t: 36, b: 36 }},
    xaxis: {{ showgrid: false, linecolor: gridColor }},
    yaxis: {{ range: [0, 310000], gridcolor: gridColor, zeroline: false }},
    legend: {{ orientation: "h", y: 1.12, x: 0 }}
  }}, cfg);

  // Chart 2: 7-Platform Donut Structure
  const pv = d.pie_views;
  Plotly.newPlot("chart-platform-donut", [{{
    type: "pie",
    labels: pv.map(x => x.name),
    values: pv.map(x => x.value),
    hole: 0.56,
    textinfo: "percent",
    textposition: "inside",
    marker: {{
      colors: ["#E11D48", "#10B981", "#38BDF8", "#F59E0B", "#8B5CF6", "#64748B"],
      line: {{ color: "#10131C", width: 2 }}
    }}
  }}], {{
    paper_bgcolor: paperBg, plot_bgcolor: plotBg, font: fontCfg,
    height: 340,
    margin: {{ l: 12, r: 12, t: 24, b: 24 }},
    showlegend: true,
    legend: {{ orientation: "h", y: -0.15, x: 0, font: {{ size: 11 }} }},
    annotations: [{{ text: "<b>48.1萬</b><br>全網觸及", x: 0.5, y: 0.5, showarrow: false, font: {{ size: 13, color: "#F8FAFC" }} }}]
  }}, cfg);

  // Chart 3: Audience Sentiment & Topic Polarity
  const cats = [
    {{ label: "正向期待 (A-Lin主題曲/陳冲卡司/屍憶導演)", val: 68 }},
    {{ label: "好奇懸疑 (詢問真實事件/買命黑幕設定)", val: 24 }},
    {{ label: "觀望中立 (預告剪輯節奏/縮網址討論)", val: 8 }}
  ];
  Plotly.newPlot("chart-sentiment-bar", [{{
    type: "bar",
    orientation: "h",
    y: cats.map(c => c.label),
    x: cats.map(c => c.val),
    text: cats.map(c => c.val + "%"),
    textposition: "outside",
    marker: {{ color: ["#10B981", "#F59E0B", "#E11D48"], line: {{ width: 0 }} }}
  }}], {{
    paper_bgcolor: paperBg, plot_bgcolor: plotBg, font: fontCfg,
    height: 300,
    margin: {{ l: 210, r: 44, t: 20, b: 30 }},
    xaxis: {{ range: [0, 82], gridcolor: gridColor, ticksuffix: "%" }},
    yaxis: {{ automargin: true }}
  }}, cfg);
}}

document.addEventListener("DOMContentLoaded", renderCharts);
"""

with open(os.path.join(BASE_DIR, "docs", "dashboard.js"), "w", encoding="utf-8") as f:
    f.write(js_code)

html_out = f"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《消失的金鳳娜》THE EVIL INSIDE｜即時聲量戰情室</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Noto+Sans+TC:wght@400;500;600;700;800&family=Noto+Serif+TC:wght@600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js" defer></script>
<script src="dashboard.js" defer></script>
<style>
:root {{
  /* Layer 1: Primitive Tokens */
  --raw-obsidian-950: #08090E;
  --raw-velvet-900: #10131C;
  --raw-velvet-800: #171B28;
  --raw-velvet-700: #1F2435;
  --raw-crimson-600: #E11D48;
  --raw-crimson-400: #FB7185;
  --raw-gold-500: #F59E0B;
  --raw-gold-300: #FCD34D;
  --raw-emerald-500: #10B981;
  --raw-emerald-300: #6EE7B7;
  --raw-red-500: #EF4444;
  --raw-cyan-400: #38BDF8;
  --raw-ivory-50: #F8FAFC;
  --raw-slate-200: #E2E8F0;
  --raw-slate-400: #94A3B8;

  /* Layer 2: Semantic Tokens */
  --bg-canvas: #08090E;
  --surface-1: #10131C;
  --surface-2: #171B28;
  --surface-3: #1F2435;
  --accent-crimson: #E11D48;
  --accent-gold: #F59E0B;
  --accent-telemetry: #38BDF8;
  --status-growth: #10B981;
  --status-flat: #F59E0B;
  --status-decline: #EF4444;
  --text-primary: #F8FAFC;
  --text-secondary: #E2E8F0;
  --text-muted: #94A3B8;
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.16);

  /* Layer 3: Component Tokens */
  --font-sans: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-serif: 'Noto Serif TC', serif;
  --font-mono: 'Fira Code', 'JetBrains Mono', monospace;
  --card-radius: 14px;
  --nav-bg: rgba(8, 9, 14, 0.88);
}}

* {{ box-sizing: border-box; }}
html {{
  scroll-behavior: smooth;
  scroll-padding-top: 92px;
}}
body {{
  margin: 0;
  padding: 0;
  background-color: var(--bg-canvas);
  background-image:
    radial-gradient(circle at 12% 8%, rgba(225, 29, 72, 0.10), transparent 32%),
    radial-gradient(circle at 88% 14%, rgba(245, 158, 11, 0.08), transparent 30%);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}}

a, button, input, summary {{
  transition: all 180ms ease;
}}
a:focus-visible, button:focus-visible, input:focus-visible, summary:focus-visible {{
  outline: 2px solid var(--accent-gold);
  outline-offset: 2px;
}}

/* Sticky Top Command Bar */
.command-bar {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--nav-bg);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border-subtle);
  padding: 10px 24px;
}}
.command-inner {{
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}}
.brand-cluster {{
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}}
.brand-mark {{
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--accent-crimson);
  box-shadow: 0 0 12px var(--accent-crimson);
  flex-shrink: 0;
}}
.brand-title {{
  font-family: var(--font-serif);
  font-weight: 800;
  font-size: 1.05rem;
  color: var(--text-primary);
  letter-spacing: 0.02em;
}}
.countdown-pill {{
  background: rgba(225, 29, 72, 0.16);
  color: #FDA4AF;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
  font-family: var(--font-mono);
}}
.nav-links {{
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}}
.nav-link {{
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.84rem;
  font-weight: 600;
  padding: 8px 11px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  border-radius: 8px;
}}
.nav-link:hover {{
  background: var(--surface-2);
  color: var(--accent-gold);
}}
.action-cluster {{
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}}
.cmd-btn {{
  min-height: 44px;
  padding: 8px 13px;
  border-radius: 9px;
  background: var(--surface-2);
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  font-size: 0.82rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}}
.cmd-btn:hover {{
  background: var(--surface-3);
  border-color: var(--accent-gold);
  color: var(--accent-gold);
}}
.cmd-btn-primary {{
  background: rgba(225, 29, 72, 0.2);
  border-color: rgba(225, 29, 72, 0.45);
  color: #FFE4E6;
}}

/* Main Container */
.main-wrap {{
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 24px 72px 24px;
}}

/* Snapshot Bar */
.snapshot-bar {{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}}
.snapshot-label {{
  font-size: 0.86rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
}}
.snapshot-pills {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}}
.snap-btn {{
  min-height: 44px;
  padding: 8px 14px;
  border-radius: 999px;
  background: var(--surface-1);
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
  font-family: var(--font-mono);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
}}
.snap-btn.active, .snap-btn:hover {{
  background: rgba(245, 158, 11, 0.16);
  color: var(--raw-gold-300);
  border-color: rgba(245, 158, 11, 0.45);
}}

/* Bento Grid */
.bento-grid {{
  display: grid;
  grid-template-columns: 1.35fr repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 36px;
}}
.bento-hero {{
  grid-row: span 2;
  background: linear-gradient(150deg, #131724 0%, #191222 65%, #23111E 100%);
  border: 1px solid var(--border-strong);
  border-radius: var(--card-radius);
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.hero-tag {{
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--raw-gold-300);
  letter-spacing: 0.04em;
  margin-bottom: 8px;
}}
.hero-main-title {{
  font-family: var(--font-serif);
  font-size: 1.45rem;
  font-weight: 800;
  line-height: 1.38;
  margin: 0 0 12px 0;
  color: var(--text-primary);
}}
.hero-big-num {{
  font-family: var(--font-mono);
  font-size: 2.75rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.15;
  margin-bottom: 8px;
}}
.hero-delta-pill {{
  display: inline-block;
  background: rgba(16, 185, 129, 0.16);
  color: var(--raw-emerald-300);
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 999px;
  margin-bottom: 14px;
}}
.hero-desc {{
  font-size: 0.92rem;
  color: var(--text-secondary);
  line-height: 1.68;
  max-width: 56ch;
  margin: 0 0 16px 0;
}}
.contrib-bar-wrap {{
  margin-top: auto;
}}
.contrib-label {{
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 6px;
  display: flex;
  justify-content: space-between;
}}
.contrib-bar {{
  height: 8px;
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
  overflow: hidden;
  display: flex;
}}
.contrib-seg-yt {{ width: 75%; background: var(--accent-telemetry); }}
.contrib-seg-th {{ width: 15%; background: var(--status-growth); }}
.contrib-seg-other {{ width: 10%; background: var(--accent-gold); }}

.bento-card {{
  background: var(--surface-1);
  border: 1px solid var(--border-subtle);
  border-radius: var(--card-radius);
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.bento-card:hover {{
  background: var(--surface-2);
}}
.card-top {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
}}
.card-label {{
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--text-secondary);
  line-height: 1.4;
}}
.card-icon {{
  width: 20px;
  height: 20px;
  color: var(--accent-gold);
  flex-shrink: 0;
}}
.card-val {{
  font-family: var(--font-mono);
  font-size: 1.55rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.25;
  margin-bottom: 8px;
}}
.card-delta {{
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--raw-emerald-300);
  margin-bottom: 10px;
}}
.mini-progress {{
  height: 5px;
  background: rgba(255,255,255,0.07);
  border-radius: 999px;
  overflow: hidden;
}}
.mini-progress-fill {{
  height: 100%;
  background: linear-gradient(90deg, var(--status-growth), var(--accent-telemetry));
  border-radius: 999px;
}}

/* Section Headers */
.sec-head {{
  margin-top: 36px;
  margin-bottom: 16px;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 12px;
}}
.sec-title {{
  font-family: var(--font-serif);
  font-size: 1.38rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  line-height: 1.38;
}}
.sec-sub {{
  font-size: 0.9rem;
  color: var(--text-muted);
  margin: 0;
  line-height: 1.65;
  max-width: 58ch;
}}

/* Controls & Filter Pills */
.controls-row {{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 14px;
}}
.pill-group {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}}
.pill-btn {{
  min-height: 44px;
  padding: 8px 14px;
  border-radius: 999px;
  background: var(--surface-1);
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
  font-size: 0.83rem;
  font-weight: 600;
  cursor: pointer;
}}
.pill-btn.active, .pill-btn:hover {{
  background: var(--surface-3);
  color: var(--accent-gold);
  border-color: var(--accent-gold);
}}

/* Data Tables (No nested card borders) */
.table-wrap {{
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  background: var(--surface-1);
  border: 1px solid var(--border-subtle);
  border-radius: var(--card-radius);
  margin-bottom: 28px;
}}
.data-table {{
  width: 100%;
  min-width: 820px;
  border-collapse: collapse;
  font-size: 0.9rem;
}}
.data-table th {{
  background: var(--surface-2);
  color: var(--text-secondary);
  font-weight: 700;
  font-size: 0.82rem;
  padding: 13px 14px;
  text-align: left;
  border-bottom: 1px solid var(--border-strong);
}}
.data-table td {{
  padding: 12px 14px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  line-height: 1.55;
}}
.data-table tr:hover td {{
  background: rgba(255, 255, 255, 0.025);
}}
.col-num {{
  text-align: right !important;
  font-family: var(--font-mono);
}}
.col-center {{
  text-align: center !important;
}}
.col-metric {{
  font-weight: 600;
  color: var(--text-primary);
}}
.col-highlight {{
  font-weight: 700;
  color: var(--accent-telemetry);
}}
.col-delta-text {{
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--raw-emerald-300);
}}
.col-author {{
  font-family: var(--font-mono);
  color: var(--accent-telemetry);
  font-weight: 600;
}}
.pf-tag {{
  display: inline-block;
  background: var(--surface-2);
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.8rem;
  padding: 4px 10px;
  border-radius: 6px;
  white-space: nowrap;
}}
.chip-tag {{
  display: inline-block;
  background: var(--surface-2);
  color: var(--raw-gold-300);
  font-size: 0.78rem;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 6px;
}}
.cell-today-green {{
  background: rgba(16, 185, 129, 0.14) !important;
  color: var(--raw-emerald-300) !important;
  font-weight: 700 !important;
}}
.cell-today-yellow {{
  background: rgba(245, 158, 11, 0.14) !important;
  color: var(--raw-gold-300) !important;
  font-weight: 700 !important;
}}
.cell-today-red {{
  background: rgba(239, 68, 68, 0.14) !important;
  color: #FCA5A5 !important;
  font-weight: 700 !important;
}}
.status-pill {{
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
  white-space: nowrap;
}}
.status-pill-green {{
  background: rgba(16, 185, 129, 0.16);
  color: var(--raw-emerald-300);
}}
.status-pill-yellow {{
  background: rgba(245, 158, 11, 0.16);
  color: var(--raw-gold-300);
}}
.status-pill-red {{
  background: rgba(239, 68, 68, 0.16);
  color: #FCA5A5;
}}

/* Heatmap View Mode Toggle Rules */
#heatmap-table.mode-values .col-delta {{ display: none; }}
#heatmap-table.mode-deltas .col-val {{ display: none; }}

/* Charts 2x2 Grid */
.charts-grid {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
  margin-bottom: 36px;
}}
.chart-surface {{
  background: var(--surface-1);
  border: 1px solid var(--border-subtle);
  border-radius: var(--card-radius);
  padding: 18px;
}}
.chart-title {{
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px 0;
  line-height: 1.4;
}}
.chart-sub {{
  font-size: 0.82rem;
  color: var(--text-muted);
  margin: 0 0 10px 0;
  line-height: 1.55;
}}

/* Promo Assets Showcase Section */
.promo-grid {{
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}}
.promo-panel {{
  background: var(--surface-1);
  border: 1px solid var(--border-subtle);
  border-radius: var(--card-radius);
  padding: 20px;
}}
.cover-gallery-vertical {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  margin-top: 12px;
}}
.cover-gallery-horizontal {{
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
  margin-top: 12px;
}}
.media-item {{
  background: var(--surface-2);
  border-radius: 10px;
  padding: 12px;
}}
.media-item img {{
  width: 100%;
  height: auto;
  border-radius: 8px;
  display: block;
  margin-bottom: 10px;
}}
.media-title {{
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  line-height: 1.45;
}}
.media-actions {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}}
.media-btn {{
  min-height: 44px;
  padding: 6px 12px;
  border-radius: 8px;
  background: rgba(225, 29, 72, 0.18);
  color: #FFE4E6;
  font-size: 0.8rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}}
.media-btn:hover {{
  background: var(--accent-crimson);
  color: #FFFFFF;
}}
.media-btn-sec {{
  background: var(--surface-3);
  color: var(--text-secondary);
}}

/* Granular Details Section */
.search-bar-wrap {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}}
.search-input {{
  flex: 1;
  min-width: 240px;
  min-height: 44px;
  background: var(--surface-1);
  border: 1px solid var(--border-strong);
  border-radius: 10px;
  padding: 10px 14px;
  color: var(--text-primary);
  font-size: 0.9rem;
}}
.tab-bar {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
}}
.tab-btn {{
  min-height: 44px;
  padding: 8px 16px;
  border-radius: 10px;
  background: var(--surface-1);
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
  font-size: 0.86rem;
  font-weight: 700;
  cursor: pointer;
}}
.tab-btn.active, .tab-btn:hover {{
  background: rgba(56, 189, 248, 0.16);
  color: var(--accent-telemetry);
  border-color: var(--accent-telemetry);
}}
.detail-tab-pane {{
  display: none;
}}
.detail-tab-pane.active {{
  display: block;
}}
.comment-link, .action-link {{
  color: var(--accent-telemetry);
  text-decoration: none;
}}
.comment-link:hover, .action-link:hover {{
  text-decoration: underline;
}}
.dcard-summary-list {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}}
.dcard-box {{
  background: var(--surface-1);
  border: 1px solid var(--border-subtle);
  border-radius: var(--card-radius);
  padding: 18px;
}}
.dcard-box h4 {{
  margin: 0 0 8px 0;
  font-size: 0.98rem;
  line-height: 1.45;
  color: var(--text-primary);
}}
.dcard-box p {{
  margin: 0 0 8px 0;
  font-size: 0.88rem;
  line-height: 1.65;
  color: var(--text-secondary);
  max-width: 58ch;
}}

@media (max-width: 1120px) {{
  .bento-grid {{
    grid-template-columns: repeat(2, 1fr);
  }}
  .bento-hero {{
    grid-column: span 2;
    grid-row: span 1;
  }}
  .charts-grid, .promo-grid, .dcard-summary-list {{
    grid-template-columns: 1fr;
  }}
}}

@media (max-width: 680px) {{
  .command-bar {{
    padding: 8px 14px;
  }}
  .main-wrap {{
    padding: 16px 14px 56px 14px;
  }}
  .bento-grid {{
    grid-template-columns: 1fr;
  }}
  .bento-hero {{
    grid-column: span 1;
    padding: 18px;
  }}
  .hero-big-num {{
    font-size: 2.1rem;
  }}
  .cover-gallery-vertical {{
    grid-template-columns: 1fr;
  }}
}}

@media (prefers-reduced-motion: reduce) {{
  *, ::before, ::after {{
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }}
}}
</style>
</head>
<body>

<!-- Sticky Top Command Bar -->
<header class="command-bar">
  <div class="command-inner">
    <div class="brand-cluster">
      <span class="brand-mark" aria-hidden="true"></span>
      <span class="brand-title">《消失的金鳳娜》THE EVIL INSIDE｜即時聲量戰情室</span>
      <span class="countdown-pill">距離 10/29 全台上映倒數 5 天</span>
    </div>
    <nav class="nav-links" aria-label="快速跳轉導覽">
      <a href="#kpi-overview" class="nav-link">總覽 KPI</a>
      <a href="#heatmap-matrix" class="nav-link">🟢🟡🔴 成長熱力矩陣</a>
      <a href="#trend-charts" class="nav-link">跨日趨勢與結構</a>
      <a href="#promo-assets" class="nav-link">最新獨家新聞風短影音</a>
      <a href="#granular-details" class="nav-link">各平台明細檢索</a>
    </nav>
    <div class="action-cluster">
      <a href="https://docs.google.com/document/d/1z7PpN7NUAPNbIbgudac8pk2u1UDQN0Zl3PR3QU2Td8c/edit" target="_blank" rel="noopener" class="cmd-btn">📄 Google Doc 完整報告</a>
      <a href="https://drive.google.com/drive/folders/11SylHSl5MFqaNkOYBsMldIR3CKWVZIWf" target="_blank" rel="noopener" class="cmd-btn">📁 專案雲端硬碟</a>
      <button type="button" onclick="exportCSV()" class="cmd-btn cmd-btn-primary">⬇ 匯出 CSV</button>
    </div>
  </div>
</header>

<main class="main-wrap">

  <!-- Date Snapshot Selector -->
  <div class="snapshot-bar" id="kpi-overview">
    <div class="snapshot-label" id="hero-snap-badge">最後同步：{data['last_updated']}</div>
    <div class="snapshot-pills" role="group" aria-label="歷史日期快照切換">
      <button type="button" class="snap-btn active" onclick="switchSnapshot('2026-10-24', this)">2026-10-24 最新</button>
      <button type="button" class="snap-btn" onclick="switchSnapshot('2026-10-23', this)">2026-10-23 發酵日</button>
      <button type="button" class="snap-btn" onclick="switchSnapshot('2026-10-22', this)">2026-10-22 首映日</button>
    </div>
  </div>

  <!-- Bento Hero + 5 Secondary KPI Cards -->
  <section class="bento-grid" aria-label="核心聲量指標">
    <div class="bento-hero">
      <div>
        <div class="hero-tag">CROSS-PLATFORM TOTAL BUZZ &amp; REACH</div>
        <h1 class="hero-main-title">全網跨平台累計總觸及與互動聲量</h1>
        <div class="hero-big-num" id="hero-total-val">481,648</div>
        <span class="hero-delta-pill" id="hero-total-delta">🟢 +71,298 (+17.4%) vs 昨日</span>
        <p class="hero-desc" id="hero-sub-text">
          核心預告與社群擴散總聲量 264,347（單日 +62,252 / +30.8%），加計新聞媒體與外部長短影音跨平台總觸及達 481,648 次。
        </p>
      </div>
      <div class="contrib-bar-wrap">
        <div class="contrib-label">
          <span>平台貢獻結構：YouTube 75% ｜ Threads 15% ｜ FB/IG/新聞 10%</span>
          <span>100%</span>
        </div>
        <div class="contrib-bar">
          <div class="contrib-seg-yt"></div>
          <div class="contrib-seg-th"></div>
          <div class="contrib-seg-other"></div>
        </div>
      </div>
    </div>

    <!-- Secondary Card 1 -->
    <div class="bento-card">
      <div>
        <div class="card-top">
          <span class="card-label">YouTube 預告與花絮總觀看</span>
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
        </div>
        <div class="card-val" id="kpi-val-0">198,208</div>
        <div class="card-delta" id="kpi-delta-0">🟢 +53,751 (+37.2%)</div>
      </div>
      <div class="mini-progress"><div class="mini-progress-fill" id="kpi-bar-0" style="width:84%;"></div></div>
    </div>

    <!-- Secondary Card 2 -->
    <div class="bento-card">
      <div>
        <div class="card-top">
          <span class="card-label">FB 雙粉專與演員貼文互動量</span>
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle></svg>
        </div>
        <div class="card-val" id="kpi-val-1">1,116 人</div>
        <div class="card-delta" id="kpi-delta-1">🟢 +350 人 (+45.7%)</div>
      </div>
      <div class="mini-progress"><div class="mini-progress-fill" id="kpi-bar-1" style="width:78%;"></div></div>
    </div>

    <!-- Secondary Card 3 -->
    <div class="bento-card">
      <div>
        <div class="card-top">
          <span class="card-label">IG 官方追蹤與 Reels 互動量</span>
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><circle cx="12" cy="12" r="4"></circle></svg>
        </div>
        <div class="card-val" id="kpi-val-2">374 粉 / 757 互動</div>
        <div class="card-delta" id="kpi-delta-2">🟢 +38 粉 (+11.3%)</div>
      </div>
      <div class="mini-progress"><div class="mini-progress-fill" id="kpi-bar-2" style="width:72%;"></div></div>
    </div>

    <!-- Secondary Card 4 -->
    <div class="bento-card">
      <div>
        <div class="card-top">
          <span class="card-label">Threads @9wo0725 與脆友熱議</span>
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        </div>
        <div class="card-val" id="kpi-val-3">31.0K 瀏覽 / 1,503 互動</div>
        <div class="card-delta" id="kpi-delta-3">🟢 單篇最高 980 讚</div>
      </div>
      <div class="mini-progress"><div class="mini-progress-fill" id="kpi-bar-3" style="width:88%;"></div></div>
    </div>

    <!-- Secondary Card 5 -->
    <div class="bento-card" style="grid-column: span 2;">
      <div>
        <div class="card-top">
          <span class="card-label">媒體新聞與論壇（Dcard / PTT / Google Trends）擴散</span>
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
        </div>
        <div class="card-val" id="kpi-val-4">160 則新聞 ｜ PTT 15 推 ｜ Trends 熱度 80 (峰值 100)</div>
        <div class="card-delta" id="kpi-delta-4">🟢 雙片搜尋對照 48 : 18 領先《消失的她》2.7 倍</div>
      </div>
      <div class="mini-progress"><div class="mini-progress-fill" id="kpi-bar-4" style="width:80%;"></div></div>
    </div>
  </section>

  <!-- Section 1: Interactive Platform Growth Heatmap Matrix -->
  <section id="heatmap-matrix">
    <div class="sec-head">
      <div>
        <h2 class="sec-title">1. 🟢🟡🔴 跨平台聲量成長熱力矩陣</h2>
        <p class="sec-sub">支援視圖切換與平台快速篩選，直觀掌握 10/22 首映日、10/23 發酵日至 10/24 爆發日的關鍵指標漲跌。</p>
      </div>
      <div class="pill-group" role="group" aria-label="視圖模式切換">
        <button type="button" class="pill-btn hm-mode-btn active" onclick="setHeatmapViewMode('combined', this)">綜合視圖（數值＋漲跌）</button>
        <button type="button" class="pill-btn hm-mode-btn" onclick="setHeatmapViewMode('values', this)">僅看關鍵數值</button>
        <button type="button" class="pill-btn hm-mode-btn" onclick="setHeatmapViewMode('deltas', this)">僅看日增幅 Δ%</button>
      </div>
    </div>

    <div class="controls-row">
      <div class="pill-group" role="group" aria-label="燈號篩選">
        <button type="button" class="pill-btn hm-status-btn active" onclick="filterHeatmapStatus('all', this)">全部燈號 (13)</button>
        <button type="button" class="pill-btn hm-status-btn" onclick="filterHeatmapStatus('green', this)">🟢 成長 (9)</button>
        <button type="button" class="pill-btn hm-status-btn" onclick="filterHeatmapStatus('yellow', this)">🟡 持平 (3)</button>
        <button type="button" class="pill-btn hm-status-btn" onclick="filterHeatmapStatus('red', this)">🔴 下滑 (1)</button>
      </div>
    </div>

    <div class="table-wrap">
      <table class="data-table mode-combined" id="heatmap-table">
        <thead>
          <tr>
            <th>平台</th>
            <th>核心監測指標</th>
            <th class="col-num col-val">10/15 基準</th>
            <th class="col-num col-val">10/22 首映日</th>
            <th class="col-num col-val">10/23 發酵日</th>
            <th class="col-num col-val">10/24 爆發日</th>
            <th class="col-center">狀態燈號</th>
            <th class="col-delta">日增幅 Δ% 與關鍵判讀</th>
          </tr>
        </thead>
        <tbody>
          {"".join(hm_rows_html)}
        </tbody>
      </table>
    </div>
  </section>

  <!-- Section 2: Interactive Plotly Charts Grid -->
  <section id="trend-charts">
    <div class="sec-head">
      <div>
        <h2 class="sec-title">2. 跨日聲量成長趨勢與 7 大平台結構分析</h2>
        <p class="sec-sub">追蹤 10/15 至 10/24 跨日爆發斜率、7 大平台觸及結構占比、觀眾情緒極性與高頻討論文字雲。</p>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-surface">
        <h3 class="chart-title">跨日總聲量與各平台成長趨勢折線圖 (10/15 → 10/24)</h3>
        <p class="chart-sub">YouTube 長片單日暴增 +5.37 萬（+37.2%），帶動核心聲量衝上 26.4 萬</p>
        <div id="chart-trend-line"></div>
      </div>

      <div class="chart-surface">
        <h3 class="chart-title">7 大平台聲量結構佔比甜甜圈圖</h3>
        <p class="chart-sub">官方 YouTube 長短影音與 Threads 自然討論構成前三大主力動能</p>
        <div id="chart-platform-donut"></div>
      </div>

      <div class="chart-surface">
        <h3 class="chart-title">觀眾情緒極性與正負評結構分析</h3>
        <p class="chart-sub">68% 高度正向期待（聚焦 A-Lin 主題曲、陳冲母女同台與《屍憶》導演）</p>
        <div id="chart-sentiment-bar"></div>
      </div>

      <div class="chart-surface">
        <h3 class="chart-title">YouTube / Dcard / Threads 高頻討論關鍵字文字雲</h3>
        <p class="chart-sub">「陳冲、A-Lin、寶貝愛人、買命黑幕、屍憶、劉奕兒」為最高頻核心詞</p>
        <img src="assets/wordcloud_20261024.webp" alt="觀眾高頻討論文字雲" style="width:100%;height:290px;object-fit:contain;border-radius:8px;display:block;">
      </div>
    </div>
  </section>

  <!-- Section 3: Newly Produced Short Promo Video & Marketing Assets -->
  <section id="promo-assets">
    <div class="sec-head">
      <div>
        <h2 class="sec-title">3. 最新短影音與行銷素材展示區（NEWS LIVE 獨家新聞爆料風 v1）</h2>
        <p class="sec-sub">已完成 FFmpeg + Remotion 合成之 24 秒雙比例（9:16 直式與 16:9 橫式）短影音與 v3 封面圖，全數嵌入首幀與縮圖軌並開放 Google Drive 雲端下載。</p>
      </div>
    </div>

    <div class="promo-grid">
      <!-- 9:16 Vertical Cards -->
      <div class="promo-panel">
        <h3 class="chart-title">📱 9:16 直式短影音版本（1080×1920｜Reels / Shorts / TikTok / Threads）</h3>
        <p class="chart-sub">標題：《劉奕兒驚傳遭療養院設局！深陷「地下賭王」買命黑幕》（24.0 秒）</p>
        <div class="cover-gallery-vertical">
          <div class="media-item">
            <img src="assets/cover_a_9x16.webp" alt="款式 A 9:16 直式新聞直播鏡面封面" loading="lazy">
            <div class="media-title">款式 A：NEWS LIVE 電視新聞直播鏡面版 (9:16)</div>
            <div class="media-actions">
              <a href="https://drive.google.com/file/d/1gpp0uBBS9kqRLQhHjx5uvmMxV_QyuqoK/view?usp=sharing" target="_blank" rel="noopener" class="media-btn">▶ 觀看/下載 MP4 (20.4MB)</a>
              <a href="https://drive.google.com/file/d/1FjR3BCcSaz3MnywyWo_aggAuDuiC3Ot0/view?usp=sharing" target="_blank" rel="noopener" class="media-btn media-btn-sec">🖼 封面原圖</a>
            </div>
          </div>
          <div class="media-item">
            <img src="assets/cover_b_9x16.webp" alt="款式 B 9:16 直式獨家專訪社會直擊封面" loading="lazy">
            <div class="media-title">款式 B：News Live 獨家專訪社會直擊版 (9:16)</div>
            <div class="media-actions">
              <a href="https://drive.google.com/file/d/1plgDG-aAn8Am3M6lpceTXQ2bwa3W1R8Q/view?usp=sharing" target="_blank" rel="noopener" class="media-btn">▶ 觀看/下載 MP4 (20.8MB)</a>
              <a href="https://drive.google.com/file/d/1pxVVSa2RTGt6mAnzIpPMJR67bPmRpbdG/view?usp=sharing" target="_blank" rel="noopener" class="media-btn media-btn-sec">🖼 封面原圖</a>
            </div>
          </div>
        </div>
      </div>

      <!-- 16:9 Horizontal Cards + Youth Keyword Strategy Table -->
      <div class="promo-panel">
        <h3 class="chart-title">🖥️ 16:9 橫式影片版本（1920×1080｜YouTube / FB 粉專 / LINE 轉傳）</h3>
        <p class="chart-sub">同步移除真實媒體台名，統一採用 NEWS LIVE 原創鏡面視覺</p>
        <div class="cover-gallery-horizontal">
          <div class="media-item">
            <img src="assets/cover_a_16x9.webp" alt="款式 A 16:9 橫式新聞直播鏡面封面" loading="lazy">
            <div class="media-title">款式 A：NEWS LIVE 電視新聞直播鏡面版 (16:9)</div>
            <div class="media-actions">
              <a href="https://drive.google.com/file/d/1fvBn-32WJpHyQYmySBG-2Kpa4k9aGr4T/view?usp=sharing" target="_blank" rel="noopener" class="media-btn">▶ 觀看/下載 MP4 (25.0MB)</a>
              <a href="https://drive.google.com/file/d/1HhWaNuaXCQ4ASptzgl_9rzmEqqgmL8Pz/view?usp=sharing" target="_blank" rel="noopener" class="media-btn media-btn-sec">🖼 封面原圖</a>
            </div>
          </div>
          <div class="media-item">
            <img src="assets/cover_b_16x9.webp" alt="款式 B 16:9 橫式獨家專訪社會直擊封面" loading="lazy">
            <div class="media-title">款式 B：News Live 獨家專訪社會直擊版 (16:9)</div>
            <div class="media-actions">
              <a href="https://drive.google.com/file/d/1arsM8Kpfnez_zpRE2u6OqBHEorONHoLV/view?usp=sharing" target="_blank" rel="noopener" class="media-btn">▶ 觀看/下載 MP4 (25.8MB)</a>
              <a href="https://drive.google.com/file/d/1WItZLxyf-Lpasw3kZutAhB-S-mz6ecP5/view?usp=sharing" target="_blank" rel="noopener" class="media-btn media-btn-sec">🖼 封面原圖</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 18-34 Youth Marketing Strategy Replacement Keywords Table -->
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>目標受眾分層 (18–34 歲年輕族群)</th>
            <th>主打傳播鉤子與替代核心詞彙</th>
            <th>主推平台與素材配置</th>
            <th>預期轉化行動 (CTA)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="pf-tag">18–24 歲大學生與脆友</span></td>
            <td class="col-metric">「黑心療養院設局」、「166 號買命標的」、「全員黑化只有一個好人」</td>
            <td>Threads 熱門串文互動、IG Reels 9:16 獨家新聞風短影音、Dcard 台中/高雄特映口碑</td>
            <td>導流點擊完整版正式預告、揪團預約 10/29 首週場次</td>
          </tr>
          <tr>
            <td><span class="pf-tag">25–34 歲懸疑驚悚影迷</span></td>
            <td class="col-metric">「地下賭王買命黑幕」、「真實社會案件改編」、「《屍憶》導演謝庭菡暗黑新作」</td>
            <td>YouTube 30 秒預告、PTT movie 板議題推文、蕃新聞與鏡週刊深度影評</td>
            <td>觸發搜尋「消失的金鳳娜 真實事件」，拉升首週末票房轉化</td>
          </tr>
          <tr>
            <td><span class="pf-tag">華語金獎卡司與音樂受眾</span></td>
            <td class="col-metric">「國際影后陳冲 × 許文珊母女同台飆戲」、「A-Lin 獻唱洗腦主題曲《寶貝愛人》」</td>
            <td>YouTube 主題曲 MV (10/27 完整版上架)、Facebook 官方粉專與 LINE 群組 16:9 橫式短片</td>
            <td>透過 A-Lin 歌迷與影后話題破圈擴散至一般大眾觀影族群</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- Section 4: Tucked-Away Granular Details at Bottom -->
  <section id="granular-details">
    <div class="sec-head">
      <div>
        <h2 class="sec-title">4. 各平台細部數據與真實評論檢索庫</h2>
        <p class="sec-sub">提供即時關鍵字搜尋、平台快速過濾與分頁檢索，完整收錄 23 項量化指標、12 則 YouTube 留言、15 則 PTT 推文、Dcard 實測與 7 則表外新聞。</p>
      </div>
    </div>

    <div class="search-bar-wrap">
      <input type="search" id="detail-search-input" class="search-input" placeholder="🔍 輸入關鍵字即時檢索（例如：陳冲、A-Lin、30秒預告、買命黑幕、蕃新聞...）" oninput="applyDetailsSearch()">
      <div class="pill-group" role="group" aria-label="明細平台過濾">
        <button type="button" class="pill-btn detail-pf-btn active" onclick="filterDetailsGroup('ALL', this)">全部平台</button>
        <button type="button" class="pill-btn detail-pf-btn" onclick="filterDetailsGroup('YouTube', this)">YouTube</button>
        <button type="button" class="pill-btn detail-pf-btn" onclick="filterDetailsGroup('Facebook', this)">Facebook</button>
        <button type="button" class="pill-btn detail-pf-btn" onclick="filterDetailsGroup('Instagram', this)">Instagram</button>
        <button type="button" class="pill-btn detail-pf-btn" onclick="filterDetailsGroup('Threads', this)">Threads</button>
        <button type="button" class="pill-btn detail-pf-btn" onclick="filterDetailsGroup('Dcard / PTT', this)">Dcard / PTT</button>
        <button type="button" class="pill-btn detail-pf-btn" onclick="filterDetailsGroup('新聞媒體', this)">新聞媒體</button>
      </div>
    </div>

    <div class="tab-bar" role="tablist">
      <button type="button" class="tab-btn active" onclick="switchDetailTab('tab-quant', this)">📊 全平台 23 項指標逐日明細</button>
      <button type="button" class="tab-btn" onclick="switchDetailTab('tab-yt-comments', this)">💬 YouTube 12 則真實觀眾評論</button>
      <button type="button" class="tab-btn" onclick="switchDetailTab('tab-ptt-dcard', this)">🎓 PTT 15 則推文 ＆ Dcard 登入實測</button>
      <button type="button" class="tab-btn" onclick="switchDetailTab('tab-news', this)">📰 表外新增 7 則新聞與影評</button>
    </div>

    <!-- Tab 1: 23 Quantitative Metrics -->
    <div id="tab-quant" class="detail-tab-pane active">
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>平台</th>
              <th>指標項目</th>
              <th class="col-num">09/17–10/15</th>
              <th class="col-num">10/22 首映</th>
              <th class="col-num">10/23</th>
              <th class="col-num">10/24 今日</th>
              <th class="col-num">單日變化</th>
              <th class="col-center">狀態</th>
            </tr>
          </thead>
          <tbody>
            {"".join(quant_rows_html)}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 2: YouTube 12 Comments -->
    <div id="tab-yt-comments" class="detail-tab-pane">
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th class="col-center">編號</th>
              <th>所屬影片</th>
              <th>留言者</th>
              <th>留言內容（點擊開啟原片）</th>
              <th class="col-num">按讚數</th>
              <th>情緒與話題分類</th>
            </tr>
          </thead>
          <tbody>
            {"".join(ytc_rows_html)}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 3: PTT 15 Pushes & Dcard Details -->
    <div id="tab-ptt-dcard" class="detail-tab-pane">
      <div class="dcard-summary-list" style="margin-bottom:18px;">
        <div class="dcard-box">
          <h4>✅ Dcard 登入實測與話題標籤（{tag['name']}）</h4>
          <p>{dc['login_status']}</p>
          <p>收錄文章：{tag['posts']} 篇 ｜ 追蹤人數：{tag['followers']} 人（{tag['note']}）</p>
        </div>
        <div class="dcard-box">
          <h4>🌪️ 台北學生特映場颱風取消說明</h4>
          <p>{dc['typhoon_note']}</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th class="col-center">序號</th>
              <th>所屬文章</th>
              <th class="col-center">類型</th>
              <th>作者 ID</th>
              <th>PTT 推文內容</th>
            </tr>
          </thead>
          <tbody>
            {"".join(ptt_rows_html)}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 4: Extra News 7 -->
    <div id="tab-news" class="detail-tab-pane">
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th class="col-center">編號</th>
              <th class="col-num">發布日期</th>
              <th>新聞媒體</th>
              <th>報導標題與重點</th>
              <th>原文連結</th>
            </tr>
          </thead>
          <tbody>
            {"".join(news_rows_html)}
          </tbody>
        </table>
      </div>
    </div>
  </section>

</main>
</body>
</html>
"""

with open(os.path.join(BASE_DIR, "docs", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_out)

print("Generated docs/index.html size:", len(html_out), "and docs/dashboard.js size:", len(js_code))

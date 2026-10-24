# -*- coding: utf-8 -*-
import json
import base64
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

BASE_DIR = "/workspace/jinfengna_dashboard"
with open(os.path.join(BASE_DIR, "dashboard_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

wc_path = os.path.join(BASE_DIR, "3_audience_wordcloud_20261024.png")
with open(wc_path, "rb") as f:
    wc_b64 = base64.b64encode(f.read()).decode("ascii")

CHART_FONT = dict(family="Inter, Noto Sans TC, sans-serif", size=13, color="#cbd5e1")
GRID_COLOR = "rgba(148, 163, 184, 0.12)"

# 1. Google Trends Line Chart
td = data["trends_daily"]
fig_gt = go.Figure()
fig_gt.add_trace(go.Scatter(
    x=td["dates"], y=td["jinfengna_solo"],
    mode="lines+markers+text",
    name="《消失的金鳳娜》單獨熱度 (峰值100)",
    line=dict(color="#38bdf8", width=3.5, shape="spline"),
    marker=dict(size=9, color="#38bdf8", line=dict(width=2, color="#090d16")),
    text=[str(v) if v in (35, 62, 100, 95, 80) else "" for v in td["jinfengna_solo"]],
    textposition="top center",
    textfont=dict(size=12, color="#7dd3fc")
))
fig_gt.add_trace(go.Scatter(
    x=td["dates"], y=td["jinfengna_vs"],
    mode="lines+markers",
    name="雙片對照：《消失的金鳳娜》",
    line=dict(color="#10b981", width=3, shape="spline"),
    marker=dict(size=8, symbol="square", color="#10b981")
))
fig_gt.add_trace(go.Scatter(
    x=td["dates"], y=td["xiaoshideta_vs"],
    mode="lines+markers",
    name="雙片對照：《消失的她》(競品)",
    line=dict(color="#f43f5e", width=2.5, dash="dot", shape="spline"),
    marker=dict(size=7, symbol="circle", color="#f43f5e")
))
fig_gt.update_layout(
    title=dict(text="Google Trends 每日搜尋熱度趨勢與黃金交叉對照 (9/24–10/24)", font=dict(size=15, color="#f8fafc")),
    paper_bgcolor="#111827", plot_bgcolor="#111827", font=CHART_FONT,
    xaxis=dict(showgrid=False, linecolor=GRID_COLOR),
    yaxis=dict(title="相對熱度 (0–100)", range=[-6, 114], gridcolor=GRID_COLOR, zeroline=False),
    height=410, hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
    margin=dict(l=24, r=24, t=76, b=24)
)

# 2. Total Buzz Line Chart
tb = data["total_buzz_trend"]
fig_buzz = go.Figure()
fig_buzz.add_trace(go.Scatter(
    x=tb["dates"], y=tb["total_buzz"],
    mode="lines+markers+text",
    name="全網累積總聲量 (觀看+曝光+互動)",
    fill="tozeroy", fillcolor="rgba(16, 185, 129, 0.14)",
    line=dict(color="#10b981", width=4, shape="spline"),
    marker=dict(size=11, color="#10b981", line=dict(width=2, color="#090d16")),
    text=[f"{v:,}" for v in tb["total_buzz"]],
    textposition="top center", textfont=dict(size=13, color="#6ee7b7")
))
fig_buzz.add_trace(go.Scatter(
    x=tb["dates"], y=tb["yt_long"],
    mode="lines+markers", name="官方 YouTube 長片總觀看 (6支)",
    line=dict(color="#38bdf8", width=3, dash="dash", shape="spline"),
    marker=dict(size=8, color="#38bdf8")
))
fig_buzz.add_trace(go.Scatter(
    x=tb["dates"], y=tb["social_views_and_eng"],
    mode="lines+markers", name="Threads 瀏覽與社群互動合計",
    line=dict(color="#f59e0b", width=2.5, shape="spline"),
    marker=dict(size=7, color="#f59e0b")
))
fig_buzz.update_layout(
    title=dict(text="全網總聲量跨日成長折線圖（10/24 單日 +6.2萬 / +30.8% 🟢）", font=dict(size=15, color="#f8fafc")),
    paper_bgcolor="#111827", plot_bgcolor="#111827", font=CHART_FONT,
    xaxis=dict(showgrid=False, linecolor=GRID_COLOR),
    yaxis=dict(title="累積聲量數值", range=[0, 310000], gridcolor=GRID_COLOR, zeroline=False),
    height=410, hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
    margin=dict(l=24, r=24, t=76, b=24)
)

# 3. Pie Views
df_pv = pd.DataFrame(data["pie_views"])
fig_pv = px.pie(
    df_pv, names="name", values="value", hole=0.52,
    title="全網累積觀看與曝光來源占比（總計 258,910 次）",
    color_discrete_sequence=["#38bdf8", "#10b981", "#6366f1", "#f59e0b", "#ec4899", "#64748b"]
)
fig_pv.update_traces(textposition="inside", textinfo="percent", textfont=dict(size=13, color="#ffffff"), marker=dict(line=dict(color="#111827", width=2.5)))
fig_pv.update_layout(
    title=dict(font=dict(size=15, color="#f8fafc")),
    paper_bgcolor="#111827", plot_bgcolor="#111827", font=CHART_FONT, height=380,
    legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
    margin=dict(l=16, r=120, t=56, b=16),
    annotations=[dict(text="<b>25.9萬</b><br>總觀看曝光", x=0.5, y=0.5, font_size=14, showarrow=False, font_color="#f8fafc")]
)

# 4. Pie Engagement
df_pe = pd.DataFrame(data["pie_engagement"])
fig_pe = px.pie(
    df_pe, names="name", values="value", hole=0.52,
    title="社群自然討論與貼文實質互動占比（Threads 占 59.5% 主力）",
    color_discrete_sequence=["#10b981", "#f43f5e", "#3b82f6", "#f59e0b", "#a855f7", "#64748b"]
)
fig_pe.update_traces(textposition="inside", textinfo="percent", textfont=dict(size=13, color="#ffffff"), marker=dict(line=dict(color="#111827", width=2.5)))
fig_pe.update_layout(
    title=dict(font=dict(size=15, color="#f8fafc")),
    paper_bgcolor="#111827", plot_bgcolor="#111827", font=CHART_FONT, height=380,
    legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
    margin=dict(l=16, r=120, t=56, b=16),
    annotations=[dict(text="<b>2,526次</b><br>實質互動", x=0.5, y=0.5, font_size=14, showarrow=False, font_color="#f8fafc")]
)

# 5. YT Comment Category Bar
df_ytc = pd.DataFrame(data["youtube_comments_12"])
cat_counts = df_ytc.groupby("情緒與話題分類", as_index=False).agg(則數=("編號", "count"), 總按讚=("按讚數", "sum")).sort_values("則數", ascending=True)
fig_cat = px.bar(
    cat_counts, x="則數", y="情緒與話題分類", orientation="h", text="則數", color="情緒與話題分類",
    title="12 則評論話題分布（主題曲與懸疑期待居首）",
    color_discrete_sequence=["#6366f1", "#f59e0b", "#a855f7", "#38bdf8", "#10b981"]
)
fig_cat.update_traces(textposition="outside", marker_line_width=0)
fig_cat.update_layout(
    title=dict(font=dict(size=14, color="#f8fafc")),
    paper_bgcolor="#111827", plot_bgcolor="#111827", font=CHART_FONT,
    xaxis=dict(range=[0, 5.2], showgrid=True, gridcolor=GRID_COLOR), yaxis=dict(title=""),
    height=265, showlegend=False, margin=dict(l=12, r=24, t=46, b=16)
)

# 6. YT Comment Video Bar
vid_counts = df_ytc.groupby("所屬影片", as_index=False).agg(留言則數=("編號", "count"), 累計按讚=("按讚數", "sum"))
fig_vid = px.bar(
    vid_counts, x="所屬影片", y=["留言則數", "累計按讚"], barmode="group",
    title="各支預告與主題曲：留言則數 vs 累計按讚",
    color_discrete_sequence=["#38bdf8", "#10b981"]
)
fig_vid.update_layout(
    title=dict(font=dict(size=14, color="#f8fafc")),
    paper_bgcolor="#111827", plot_bgcolor="#111827", font=CHART_FONT,
    xaxis=dict(title="", showgrid=False), yaxis=dict(title="", gridcolor=GRID_COLOR),
    height=265, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=""),
    margin=dict(l=12, r=16, t=52, b=16)
)

div_gt = fig_gt.to_html(full_html=False, include_plotlyjs="cdn", config={"responsive": True, "displayModeBar": False})
div_buzz = fig_buzz.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_pv = fig_pv.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_pe = fig_pe.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_cat = fig_cat.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_vid = fig_vid.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})

kpi_cards_html = '<div class="kpi-grid">'
for item in data["kpi_cards"]:
    delta_cls = "kpi-delta-green" if item.get("status") == "green" else "kpi-delta-amber"
    kpi_cards_html += (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{item["label"]}</div>'
        f'<div class="kpi-value">{item["value"]}</div>'
        f'<span class="{delta_cls}">{item["delta"]}</span>'
        f'</div>'
    )
kpi_cards_html += '</div>'

hm_rows_html = []
for r in data["heatmap_rows"]:
    st_label = r["狀態燈號"]
    if "🟢" in st_label:
        status_code = "green"
        today_cls = "today-cell-green"
        badge_html = f"<span class='badge-green'>{st_label}</span>"
    elif "🟡" in st_label:
        status_code = "yellow"
        today_cls = "today-cell-yellow"
        badge_html = f"<span class='badge-yellow'>{st_label}</span>"
    else:
        status_code = "red"
        today_cls = "today-cell-red"
        badge_html = f"<span class='badge-red'>{st_label}</span>"
    hm_rows_html.append(
        f"<tr class='hm-row' data-status='{status_code}'>"
        f"<td><span class='platform-pill'>{r['平台']}</span></td>"
        f"<td style='font-weight:600;color:#f8fafc;'>{r['核心指標']}</td>"
        f"<td class='num-col' style='color:#94a3b8;'>{r.get('10/15', r.get('09/17–10/15', ''))}</td>"
        f"<td class='num-col' style='color:#cbd5e1;'>{r.get('10/22 首映', r.get('2026-10-22', ''))}</td>"
        f"<td class='num-col' style='color:#cbd5e1;'>{r.get('10/23', r.get('2026-10-23', ''))}</td>"
        f"<td class='num-col {today_cls}'>{r.get('10/24 今日', r.get('2026-10-24', ''))}</td>"
        f"<td class='center-col'>{badge_html}</td>"
        f"<td style='color:#cbd5e1;'>{r['關鍵數字與判讀']}</td>"
        f"</tr>"
    )

dc = data["dcard_details"]
tag = dc["topic_tag"]
dcard_html = f"""
<div class='info-card' style='border-left: 4px solid #10b981;'>
  <div class='info-card-title'>✅ Dcard 登入與搜尋狀態</div>
  <div style='color:#cbd5e1;font-size:0.93rem;'>{dc['login_status']}</div>
</div>
<div class='info-card' style='border-left: 4px solid #38bdf8;'>
  <div class='info-card-title'>🏷️ 話題標籤（1 個）：<a href='{tag['url']}' target='_blank' style='color:#38bdf8;text-decoration:none;'>{tag['name']}</a></div>
  <span class='metric-chip'>📄 收錄文章：{tag['posts']} 篇</span>
  <span class='metric-chip'>👥 追蹤人數：{tag['followers']} 人</span>
  <div style='margin-top:10px;color:#94a3b8;font-size:0.9rem;'>{tag['note']}</div>
</div>
"""
for idx_p, p in enumerate(dc["posts"], 1):
    dcard_html += f"""
    <div class='info-card'>
      <div class='info-card-title'>📄 官方特映文 {idx_p}｜{p['board']}：<a href='{p['url']}' target='_blank' style='color:#38bdf8;text-decoration:none;'>{p['title']}</a></div>
      <div style='color:#94a3b8;font-size:0.86rem;margin-bottom:8px;'>發文單位：{p['author']} ｜ 發布時間：{p['date']} ｜ 標籤：{' '.join(p['tags'])}</div>
      <span class='metric-chip'>❤️ 愛心 {p['hearts']}</span>
      <span class='metric-chip'>💬 留言 {p['comments']}</span>
      <span class='metric-chip'>🔖 收藏 {p['bookmarks']}</span>
      <span class='metric-chip'>🔗 分享 {p['shares']}</span>
      <div style='margin-top:10px;color:#cbd5e1;font-size:0.92rem;'><b>留言區實測：</b>{p['comment_detail']}</div>
    </div>
    """
dcard_html += f"""
<div class='info-card' style='border-left: 4px solid #f59e0b;background-color:rgba(245, 158, 11, 0.06);'>
  <div class='info-card-title' style='color:#fbbf24;'>🌪️ 為什麼 Dcard 尚無學生映後文？</div>
  <div style='color:#e2e8f0;font-size:0.92rem;'>{dc['typhoon_note']}</div>
</div>
"""

ytc_rows = []
for c in data["youtube_comments_12"]:
    ytc_rows.append(
        f"<tr>"
        f"<td class='center-col'>{c['編號']}</td>"
        f"<td><span class='platform-pill'>{c['所屬影片']}</span></td>"
        f"<td style='color:#38bdf8;font-weight:600;'>{c['留言者']}</td>"
        f"<td style='color:#f8fafc;'>{c['留言內容']}</td>"
        f"<td class='center-col' style='color:#34d399;font-weight:700;'>👍 {c['按讚數']}</td>"
        f"<td><span class='metric-chip'>{c['情緒與話題分類']}</span></td>"
        f"</tr>"
    )

quant_rows = []
platforms_set = sorted(list({r["平台"] for r in data["quantitative_full_table"]}))
for r in data["quantitative_full_table"]:
    quant_rows.append(
        f"<tr class='quant-row' data-platform='{r['平台']}'>"
        f"<td><span class='platform-pill'>{r['平台']}</span></td>"
        f"<td style='font-weight:600;color:#f8fafc;'>{r['指標名稱']}</td>"
        f"<td class='num-col'>{r.get('10/15', r.get('09/17–10/15', ''))}</td>"
        f"<td class='num-col'>{r.get('10/22 首映', r.get('2026-10-22', ''))}</td>"
        f"<td class='num-col'>{r.get('10/23', r.get('2026-10-23', ''))}</td>"
        f"<td class='num-col' style='font-weight:700;color:#38bdf8;'>{r.get('10/24 今日', r.get('2026-10-24', ''))}</td>"
        f"<td class='num-col' style='color:#34d399;font-weight:600;'>{r['單日變化']}</td>"
        f"<td class='center-col'>{r['狀態']}</td>"
        f"</tr>"
    )

platform_buttons_html = "".join(
    [f'<button class="filter-btn" data-pf="{p}" onclick="filterQuant(this.getAttribute(\'data-pf\'), this)">{p}</button>' for p in platforms_set]
)

ptt_rows = []
for idx, p in enumerate(data["ptt_pushes_15"], 1):
    ptt_rows.append(
        f"<tr><td class='center-col'>{idx}</td><td>{p['文章']}</td><td class='center-col'>{p['推文類型']}</td>"
        f"<td style='color:#38bdf8;'>{p['作者']}</td><td style='color:#f8fafc;'>{p['內容']}</td></tr>"
    )

news_rows = []
for idx, n in enumerate(data["extra_news_7"], 1):
    news_rows.append(
        f"<tr><td class='center-col'>{idx}</td><td class='center-col'>{n['日期']}</td>"
        f"<td><span class='platform-pill'>{n['媒體']}</span></td><td style='color:#f8fafc;font-weight:600;'>{n['標題']}</td>"
        f"<td><a href='{n['連結']}' target='_blank' style='color:#38bdf8;'>開啟新聞連結</a></td></tr>"
    )

os.makedirs(os.path.join(BASE_DIR, "docs"), exist_ok=True)

html_out = f"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《消失的金鳳娜》每日聲量與數據分析儀表板</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700;800&family=Inter:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; }}
html, body {{
    margin: 0; padding: 0;
    font-family: 'Inter', 'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #090d16;
    color: #f1f5f9;
    -webkit-font-smoothing: antialiased;
}}
.container {{
    max-width: 1440px;
    margin: 0 auto;
    padding: 36px 40px 64px 40px;
}}
.hero-wrap {{
    background: linear-gradient(135deg, #0f172a 0%, #131c31 60%, #172554 100%);
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 18px;
    padding: 28px 34px;
    margin-bottom: 28px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
}}
.hero-top-row {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}}
.hero-eyebrow {{
    display: inline-block;
    background: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.28);
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    padding: 5px 14px;
    border-radius: 999px;
}}
.hero-links a {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.06);
    color: #e2e8f0;
    border: 1px solid rgba(148, 163, 184, 0.22);
    font-size: 0.82rem;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 8px;
    text-decoration: none;
    margin-left: 8px;
}}
.hero-links a:hover {{
    border-color: #38bdf8;
    color: #38bdf8;
}}
.hero-title {{
    font-size: 2.05rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 0 0 12px 0;
    letter-spacing: -0.01em;
    line-height: 1.25;
}}
.hero-summary {{
    font-size: 1.04rem;
    color: #cbd5e1;
    line-height: 1.75;
    margin: 0;
}}
.hero-summary b {{ color: #34d399; font-weight: 700; }}

.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(215px, 1fr));
    gap: 18px;
    margin-bottom: 36px;
}}
.kpi-card {{
    background: #111827;
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 16px;
    padding: 22px 22px 18px 22px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.22);
}}
.kpi-label {{
    font-size: 0.86rem;
    font-weight: 500;
    color: #94a3b8;
    margin-bottom: 10px;
    line-height: 1.35;
}}
.kpi-value {{
    font-size: 1.95rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin-bottom: 12px;
    font-variant-numeric: tabular-nums;
}}
.kpi-delta-green {{
    display: inline-block;
    background: rgba(16, 185, 129, 0.14);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.28);
    font-size: 0.80rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
}}
.kpi-delta-amber {{
    display: inline-block;
    background: rgba(245, 158, 11, 0.14);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.28);
    font-size: 0.80rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
}}

.section-header {{
    margin-top: 28px;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.14);
}}
.section-title {{
    font-size: 1.42rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0 0 6px 0;
}}
.section-subtitle {{
    font-size: 0.92rem;
    color: #94a3b8;
    margin: 0;
    line-height: 1.5;
}}

.filter-bar {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 16px;
}}
.filter-btn {{
    background: #111827;
    color: #cbd5e1;
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 999px;
    padding: 7px 16px;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
}}
.filter-btn:hover, .filter-btn.active {{
    background: rgba(56, 189, 248, 0.16);
    color: #38bdf8;
    border-color: #38bdf8;
}}

.table-scroll {{
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border-radius: 14px;
    border: 1px solid rgba(148, 163, 184, 0.16);
    background: #111827;
    margin-bottom: 28px;
}}
.heatmap-table {{
    width: 100%;
    min-width: 860px;
    border-collapse: collapse;
    font-size: 0.94rem;
    font-variant-numeric: tabular-nums;
}}
.heatmap-table th {{
    background-color: #1e293b;
    color: #cbd5e1;
    font-weight: 600;
    font-size: 0.84rem;
    padding: 14px 16px;
    text-align: left;
    border-bottom: 1px solid rgba(148, 163, 184, 0.22);
}}
.heatmap-table th.num-col, .heatmap-table td.num-col {{
    text-align: right;
    padding-right: 20px;
}}
.heatmap-table th.center-col, .heatmap-table td.center-col {{
    text-align: center;
}}
.heatmap-table td {{
    padding: 13px 16px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    color: #e2e8f0;
    line-height: 1.5;
}}
.heatmap-table tr:hover td {{
    background-color: rgba(255, 255, 255, 0.03);
}}
.platform-pill {{
    display: inline-block;
    background: rgba(148, 163, 184, 0.12);
    color: #f8fafc;
    font-weight: 600;
    font-size: 0.84rem;
    padding: 4px 10px;
    border-radius: 8px;
    white-space: nowrap;
}}
.today-cell-green {{
    background: rgba(16, 185, 129, 0.18) !important;
    color: #6ee7b7 !important;
    font-weight: 800 !important;
    font-size: 1.03rem !important;
}}
.today-cell-yellow {{
    background: rgba(245, 158, 11, 0.15) !important;
    color: #fcd34d !important;
    font-weight: 800 !important;
    font-size: 1.03rem !important;
}}
.today-cell-red {{
    background: rgba(239, 68, 68, 0.16) !important;
    color: #fca5a5 !important;
    font-weight: 800 !important;
    font-size: 1.03rem !important;
}}
.badge-green {{
    display: inline-block;
    background-color: rgba(16, 185, 129, 0.16);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.83rem;
    white-space: nowrap;
}}
.badge-yellow {{
    display: inline-block;
    background-color: rgba(245, 158, 11, 0.16);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.35);
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.83rem;
    white-space: nowrap;
}}
.badge-red {{
    display: inline-block;
    background-color: rgba(239, 68, 68, 0.16);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.35);
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.83rem;
    white-space: nowrap;
}}

.grid-2 {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 22px;
    margin-bottom: 24px;
}}
.grid-dcard-yt {{
    display: grid;
    grid-template-columns: 1fr 1.35fr;
    gap: 24px;
    margin-bottom: 24px;
}}
.chart-box {{
    background: #111827;
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 16px;
    padding: 12px;
    overflow: hidden;
}}
.info-card {{
    background-color: #111827;
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 14px;
    padding: 18px 20px;
    color: #e2e8f0;
    margin-bottom: 14px;
    line-height: 1.65;
}}
.info-card-title {{
    font-size: 1.02rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;
}}
.metric-chip {{
    display: inline-block;
    background: #1e293b;
    border: 1px solid rgba(148, 163, 184, 0.2);
    color: #e2e8f0;
    font-size: 0.83rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 8px;
    margin-right: 6px;
    margin-top: 4px;
}}

details.expander {{
    background: #111827;
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 14px;
    margin-bottom: 16px;
    overflow: hidden;
}}
details.expander summary {{
    padding: 16px 20px;
    font-weight: 700;
    font-size: 0.98rem;
    color: #f8fafc;
    cursor: pointer;
    background: #151e30;
    list-style: none;
}}
details.expander summary:hover {{
    color: #38bdf8;
}}
details.expander .expander-body {{
    padding: 18px 20px;
}}

@media (max-width: 1024px) {{
    .grid-2, .grid-dcard-yt {{
        grid-template-columns: 1fr;
    }}
}}
@media (max-width: 768px) {{
    .container {{
        padding: 18px 16px 48px 16px;
    }}
    .hero-wrap {{
        padding: 20px 18px;
    }}
    .hero-title {{
        font-size: 1.45rem;
    }}
    .kpi-grid {{
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }}
    .kpi-value {{
        font-size: 1.45rem;
    }}
}}
</style>
</head>
<body>
<div class="container">
    <div class="hero-wrap">
        <div class="hero-top-row">
            <span class="hero-eyebrow">⏱️ 每日自動更新儀表板 ｜ 最後同步：{data['last_updated']} ｜ 10/29 全台上映</span>
            <div class="hero-links">
                <a href="https://docs.google.com/document/d/1z7PpN7NUAPNbIbgudac8pk2u1UDQN0Zl3PR3QU2Td8c/edit" target="_blank">📄 開啟 Google Doc 完整報告</a>
                <a href="https://docs.google.com/spreadsheets/d/10Q5elsldNDSZT_l9baubBonFEqeU2uKLoZGZpKAELvw/edit" target="_blank">📊 開啟官方新聞整理表</a>
            </div>
        </div>
        <h1 class="hero-title">🎬 《消失的金鳳娜》全網聲量與數據分析儀表板</h1>
        <p class="hero-summary">
            全網累積總聲量單日成長 <b>+30.8%（202,095 ➔ 264,347）</b>，由 <b>YouTube 長片觀看暴增 +5.37 萬（+37.2%）</b>、<b>FB 談論人數跳升（+45.7%）</b> 與 <b>Threads 自然討論破千互動（單篇最高 980 讚）</b> 強勢領漲；<b>Google Trends</b> 維持首映後高檔（80–100 分）並以 <b>48 : 18（領先 2.7 倍）</b> 黃金交叉超越《消失的她》。
        </p>
    </div>

    {kpi_cards_html}

    <div class="section-header">
        <h2 class="section-title">🚦 1. 各平台聲量熱力色塊總表（按日期追蹤關鍵數字）</h2>
        <p class="section-subtitle">🟢 成長（顯著上升或突破新高，共 9 項）　｜　🟡 停滯／持平（微幅波動 &lt;5% 或待發酵，共 3 項）　｜　🔴 衰退／動能不足（共 1 項）</p>
    </div>

    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterHeatmap('all', this)">全部顯示 (13項)</button>
        <button class="filter-btn" onclick="filterHeatmap('green', this)">🟢 成長 (9項)</button>
        <button class="filter-btn" onclick="filterHeatmap('yellow', this)">🟡 停滯 (3項)</button>
        <button class="filter-btn" onclick="filterHeatmap('red', this)">🔴 衰退 (1項)</button>
    </div>

    <div class="table-scroll">
        <table class="heatmap-table">
            <thead>
                <tr>
                    <th>平台</th><th>核心指標</th><th class="num-col">10/15</th><th class="num-col">10/22 首映</th><th class="num-col">10/23</th><th class="num-col">10/24 今日最新</th><th class="center-col">狀態燈號</th><th>關鍵數字與趨勢判讀</th>
                </tr>
            </thead>
            <tbody>
                {"".join(hm_rows_html)}
            </tbody>
        </table>
    </div>

    <div class="section-header">
        <h2 class="section-title">📈 2. 總趨勢折線圖與 🥧 全網聲量圓餅占比</h2>
        <p class="section-subtitle">左圖追蹤 Google Trends 每日熱度與《消失的她》黃金交叉走勢；右圖呈現全網累積總聲量從 7.6 萬攀升至 26.4 萬的成長斜率</p>
    </div>

    <div class="grid-2">
        <div class="chart-box">{div_gt}</div>
        <div class="chart-box">{div_buzz}</div>
    </div>
    <div class="grid-2">
        <div class="chart-box">{div_pv}</div>
        <div class="chart-box">{div_pe}</div>
    </div>

    <div class="section-header">
        <h2 class="section-title">🎓 3. Dcard 登入搜尋結果專區 ＆ 💬 今日新抓 12 則 YouTube 評論視覺化</h2>
        <p class="section-subtitle">左側為「金鳳娜」Chrome 設定檔登入 Dcard 實測的 2 篇特映文與 1 個話題標籤；右側為今日新擷取的 12 則 YouTube 觀眾評論話題結構與明細</p>
    </div>

    <div class="grid-dcard-yt">
        <div>{dcard_html}</div>
        <div>
            <div class="grid-2" style="margin-bottom:16px;">
                <div class="chart-box">{div_cat}</div>
                <div class="chart-box">{div_vid}</div>
            </div>
            <div style="font-weight:700;color:#f8fafc;margin:4px 0 10px 0;font-size:0.98rem;">💬 今日新擷取 12 則 YouTube 觀眾真實評論一覽表</div>
            <div class="table-scroll" style="max-height:380px;overflow-y:auto;">
                <table class="heatmap-table" style="min-width:680px;">
                    <thead>
                        <tr><th class="center-col">編號</th><th>所屬影片</th><th>留言者</th><th>留言內容</th><th class="center-col">按讚數</th><th>情緒與話題分類</th></tr>
                    </thead>
                    <tbody>{"".join(ytc_rows)}</tbody>
                </table>
            </div>
        </div>
    </div>

    <details class="expander">
        <summary>🖼️ 點擊展開：《消失的金鳳娜》12 則 YouTube 評論 × PTT 15 則推文 × Threads 熱門口碑文字雲</summary>
        <div class="expander-body" style="text-align:center;">
            <img src="data:image/png;base64,{wc_b64}" alt="觀眾評論文字雲" style="max-width:100%;height:auto;border-radius:12px;">
        </div>
    </details>

    <div class="section-header">
        <h2 class="section-title">📋 4. 全平台指標「按日期成長」完整量化總表（23 項核心指標）</h2>
        <p class="section-subtitle">涵蓋 Google Trends、YouTube 各支影片、Threads、Instagram、Facebook、Dcard、PTT、X 與新聞媒體的逐日數值對照</p>
    </div>

    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterQuant('ALL', this)">全部平台 (23項)</button>
        {platform_buttons_html}
    </div>

    <div class="table-scroll">
        <table class="heatmap-table">
            <thead>
                <tr><th>平台</th><th>指標項目</th><th class="num-col">10/15</th><th class="num-col">10/22 首映</th><th class="num-col">10/23</th><th class="num-col">10/24 今日</th><th class="num-col">單日變化</th><th class="center-col">狀態</th></tr>
            </thead>
            <tbody>{"".join(quant_rows)}</tbody>
        </table>
    </div>

    <div class="section-header">
        <h2 class="section-title">📂 5. 細部數據備查（點擊展開查看 PTT 推文、表外新增新聞與官方 Shorts 明細）</h2>
        <p class="section-subtitle">平時收合保持版面清爽，需要核對單則推文或新聞連結時點擊即可展開</p>
    </div>

    <details class="expander">
        <summary>📌 點擊展開：PTT movie 板全部 15 則推文完整明細（2 篇文章）</summary>
        <div class="expander-body">
            <div class="table-scroll" style="margin-bottom:0;">
                <table class="heatmap-table">
                    <thead><tr><th class="center-col">序號</th><th>文章</th><th class="center-col">推文類型</th><th>作者 ID</th><th>推文內容</th></tr></thead>
                    <tbody>{"".join(ptt_rows)}</tbody>
                </table>
            </div>
        </div>
    </details>

    <details class="expander">
        <summary>📰 點擊展開：不在官方整理表（153 則）內的 7 則新增新聞與專業影評</summary>
        <div class="expander-body">
            <div class="table-scroll" style="margin-bottom:0;">
                <table class="heatmap-table">
                    <thead><tr><th class="center-col">編號</th><th class="center-col">日期</th><th>媒體</th><th>標題</th><th>原文連結</th></tr></thead>
                    <tbody>{"".join(news_rows)}</tbody>
                </table>
            </div>
        </div>
    </details>

    <details class="expander">
        <summary>📱 點擊展開：Threads 自然熱門貼文 Top 5 與官方 YouTube 11 支 Shorts 明細</summary>
        <div class="expander-body" style="line-height:1.75;color:#cbd5e1;">
            <p><b style="color:#f8fafc;">Threads 搜尋「消失的金鳳娜」熱門（Top）前 5 則：</b></p>
            <ol>
                <li><code>@jingyu4603</code>（12 小時前，一般網友）：期待陳冲，稱這是自己 2026 最好奇的國片（<b style="color:#34d399;">980 讚、35 留言、42 轉發、98 分享，共 1,155 互動</b>）</li>
                <li><code>@kimier33</code>（20 小時前，一般網友）：談 A-Lin 主題曲《寶貝愛人》10/27 上架、電影 10/29 上映（<b style="color:#34d399;">139 讚、3 留言、12 轉發、27 分享，共 181 互動</b>）</li>
                <li><code>@lingohsieh</code>（導演謝庭菡，9/25）：轉貼官方預告（<b>83 讚、2 留言、8 轉發、63 分享</b>）</li>
                <li><code>@hi_iam_littledream</code>（1 天前，一般網友）：好奇片名為何從《寶貝愛人》改成《消失的金鳳娜》（<b>17 讚、2 留言</b>）</li>
                <li><code>@aniswodimaya</code>（1 天前，一般網友）：貼海報稱「絕無冷場」（<b>12 讚、2 留言、4 轉發</b>）</li>
            </ol>
            <p><b style="color:#f8fafc;">官方 YouTube Shorts（共 11 支，合計 17,982 次觀看）：</b></p>
            <ul>
                <li>最高前四支：「天后的真面目」3,972 次、「信仰篇」2,778 次、「慈祥笑容的背後」2,222 次、「院長開示篇」1,955 次</li>
                <li>最新兩支：「上映倒數 6 天」1,100 次、「10/29 全台戲院見」955 次</li>
            </ul>
        </div>
    </details>
</div>

<script>
function filterHeatmap(status, btn) {{
    btn.parentElement.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.hm-row').forEach(row => {{
        if (status === 'all' || row.getAttribute('data-status') === status) {{
            row.style.display = '';
        }} else {{
            row.style.display = 'none';
        }}
    }});
}}
function filterQuant(platform, btn) {{
    btn.parentElement.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.quant-row').forEach(row => {{
        if (platform === 'ALL' || row.getAttribute('data-platform') === platform) {{
            row.style.display = '';
        }} else {{
            row.style.display = 'none';
        }}
    }});
}}
</script>
</body>
</html>
"""

with open(os.path.join(BASE_DIR, "docs", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_out)

print("Generated docs/index.html successfully, size:", len(html_out))

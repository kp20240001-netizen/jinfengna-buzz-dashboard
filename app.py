# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="《消失的金鳳娜》每日聲量與數據分析儀表板",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dashboard_data.json")
WC_IMG_PATH = os.path.join(BASE_DIR, "3_audience_wordcloud_20261024.png")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# ==============================================================================
# PREMIUM DESIGN SYSTEM CSS (Clean Breathing Room, Large Typography, Mobile RWD)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700;800&family=Inter:wght@500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #090d16 !important;
    color: #f1f5f9 !important;
}

/* Main container spacing & max-width for comfortable reading */
.block-container {
    max-width: 1440px !important;
    padding-top: 2.2rem !important;
    padding-bottom: 4rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

/* Hide noisy Streamlit default chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Hero Header Banner */
.hero-wrap {
    background: linear-gradient(135deg, #0f172a 0%, #131c31 60%, #172554 100%);
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 18px;
    padding: 28px 34px;
    margin-bottom: 28px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
}
.hero-eyebrow {
    display: inline-block;
    background: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.28);
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 12px;
}
.hero-title {
    font-size: 2.05rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 0 0 12px 0;
    letter-spacing: -0.01em;
    line-height: 1.25;
}
.hero-summary {
    font-size: 1.05rem;
    color: #cbd5e1;
    line-height: 1.75;
    margin: 0;
}
.hero-summary b {
    color: #34d399;
    font-weight: 700;
}

/* Responsive KPI Grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(215px, 1fr));
    gap: 18px;
    margin-bottom: 36px;
}
.kpi-card {
    background: #111827;
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 16px;
    padding: 22px 22px 18px 22px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.22);
    transition: transform 0.15s ease, border-color 0.15s ease;
}
.kpi-card:hover {
    border-color: rgba(56, 189, 248, 0.4);
}
.kpi-label {
    font-size: 0.86rem;
    font-weight: 500;
    color: #94a3b8;
    margin-bottom: 10px;
    line-height: 1.35;
}
.kpi-value {
    font-family: 'Inter', 'Noto Sans TC', sans-serif;
    font-size: 1.95rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin-bottom: 12px;
    font-variant-numeric: tabular-nums;
}
.kpi-delta-green {
    display: inline-block;
    background: rgba(16, 185, 129, 0.14);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.28);
    font-size: 0.80rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
}
.kpi-delta-amber {
    display: inline-block;
    background: rgba(245, 158, 11, 0.14);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.28);
    font-size: 0.80rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
}

/* Section Headers with generous breathing space */
.section-header {
    margin-top: 24px;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.14);
}
.section-title {
    font-size: 1.42rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}
.section-subtitle {
    font-size: 0.92rem;
    color: #94a3b8;
    margin: 0;
    line-height: 1.5;
}

/* Card Container for Charts & Tables */
.panel-card {
    background: #111827;
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 24px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.22);
}

/* Heatmap Matrix Table with horizontal scroll on mobile */
.table-scroll {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border-radius: 14px;
    border: 1px solid rgba(148, 163, 184, 0.16);
    background: #111827;
    margin-bottom: 28px;
}
.heatmap-table {
    width: 100%;
    min-width: 860px;
    border-collapse: collapse;
    font-size: 0.95rem;
    font-variant-numeric: tabular-nums;
}
.heatmap-table th {
    background-color: #1e293b;
    color: #cbd5e1;
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding: 14px 16px;
    text-align: left;
    border-bottom: 1px solid rgba(148, 163, 184, 0.22);
}
.heatmap-table th.num-col, .heatmap-table td.num-col {
    text-align: right;
    padding-right: 20px;
}
.heatmap-table th.center-col, .heatmap-table td.center-col {
    text-align: center;
}
.heatmap-table td {
    padding: 14px 16px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    color: #e2e8f0;
    line-height: 1.5;
}
.heatmap-table tr:hover td {
    background-color: rgba(255, 255, 255, 0.03);
}
.platform-pill {
    display: inline-block;
    background: rgba(148, 163, 184, 0.12);
    color: #f8fafc;
    font-weight: 600;
    font-size: 0.86rem;
    padding: 4px 10px;
    border-radius: 8px;
}
.today-cell-green {
    background: rgba(16, 185, 129, 0.18) !important;
    color: #6ee7b7 !important;
    font-weight: 800 !important;
    font-size: 1.04rem !important;
}
.today-cell-yellow {
    background: rgba(245, 158, 11, 0.15) !important;
    color: #fcd34d !important;
    font-weight: 800 !important;
    font-size: 1.04rem !important;
}
.today-cell-red {
    background: rgba(239, 68, 68, 0.16) !important;
    color: #fca5a5 !important;
    font-weight: 800 !important;
    font-size: 1.04rem !important;
}
.badge-green {
    display: inline-block;
    background-color: rgba(16, 185, 129, 0.16);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.84rem;
    white-space: nowrap;
}
.badge-yellow {
    display: inline-block;
    background-color: rgba(245, 158, 11, 0.16);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.35);
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.84rem;
    white-space: nowrap;
}
.badge-red {
    display: inline-block;
    background-color: rgba(239, 68, 68, 0.16);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.35);
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.84rem;
    white-space: nowrap;
}

/* Clean Info Cards for Dcard & Comments */
.info-card {
    background-color: #111827;
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 14px;
    padding: 18px 20px;
    color: #e2e8f0;
    margin-bottom: 14px;
    line-height: 1.65;
}
.info-card-title {
    font-size: 1.02rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;
}
.metric-chip {
    display: inline-block;
    background: #1e293b;
    border: 1px solid rgba(148, 163, 184, 0.2);
    color: #e2e8f0;
    font-size: 0.84rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 8px;
    margin-right: 8px;
    margin-top: 4px;
}

/* Mobile Responsive Adjustments */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1.2rem !important;
    }
    .hero-wrap {
        padding: 20px 18px;
    }
    .hero-title {
        font-size: 1.45rem;
    }
    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }
    .kpi-value {
        font-size: 1.45rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Sidebar (collapsed by default so main view has maximum breathing room)
with st.sidebar:
    st.markdown("### 🎬 《消失的金鳳娜》")
    st.caption(f"全台上映日：**{data['release_date']}**（大昇影業／威視發行）")
    st.caption(f"最後更新：**{data['last_updated']}**")
    if st.button("🔄 立即重新載入最新數據", use_container_width=True):
        st.rerun()
    st.markdown("---")
    st.markdown("📄 **雲端同步報告：**")
    st.markdown("- [開啟 Google Doc 完整報告](https://docs.google.com/document/d/1z7PpN7NUAPNbIbgudac8pk2u1UDQN0Zl3PR3QU2Td8c/edit)")
    st.markdown("- [開啟官方新聞露出整理表](https://docs.google.com/spreadsheets/d/10Q5elsldNDSZT_l9baubBonFEqeU2uKLoZGZpKAELvw/edit)")
    st.caption("⏰ 每日 09:00（台北時間）例行排程執行時，本儀表板資料檔自動同步刷新。")

# ==============================================================================
# HERO BANNER & TOP 6 KPI CARDS
# ==============================================================================
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-eyebrow">⏱️ 每日自動更新儀表板 ｜ 最後同步：{data['last_updated']} ｜ 10/29 全台上映</div>
    <h1 class="hero-title">🎬 《消失的金鳳娜》全網聲量與數據分析儀表板</h1>
    <p class="hero-summary">
        全網累積總聲量單日成長 <b>+30.8%（202,095 ➔ 264,347）</b>，由 <b>YouTube 長片觀看暴增 +5.37 萬（+37.2%）</b>、<b>FB 談論人數跳升（+45.7%）</b> 與 <b>Threads 自然討論破千互動（單篇最高 980 讚）</b> 強勢領漲；<b>Google Trends</b> 維持首映後高檔（80–100 分）並以 <b>48 : 18（領先 2.7 倍）</b> 黃金交叉超越《消失的她》。
    </p>
</div>
""", unsafe_allow_html=True)

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
st.markdown(kpi_cards_html, unsafe_allow_html=True)

# ==============================================================================
# SECTION 1: 🚦 熱力色塊總表（紅黃綠三色標示成長、停滯、衰退，只列關鍵數字）
# ==============================================================================
st.markdown("""
<div class="section-header">
    <h2 class="section-title">🚦 1. 各平台聲量熱力色塊總表（按日期追蹤關鍵數字）</h2>
    <p class="section-subtitle">🟢 成長（顯著上升或突破新高，共 9 項）　｜　🟡 停滯／持平（微幅波動 &lt;5% 或待發酵，共 3 項）　｜　🔴 衰退／動能不足（共 1 項）</p>
</div>
""", unsafe_allow_html=True)

filter_status = st.radio(
    "篩選燈號狀態",
    ["全部顯示 (13項)", "🟢 成長 (9項)", "🟡 停滯 (3項)", "🔴 衰退 (1項)"],
    horizontal=True,
    label_visibility="collapsed"
)

html_rows = []
for r in data["heatmap_rows"]:
    st_label = r["狀態燈號"]
    if "🟢" in filter_status and "🟢" not in st_label:
        continue
    if "🟡" in filter_status and "🟡" not in st_label:
        continue
    if "🔴" in filter_status and "🔴" not in st_label:
        continue

    if "🟢" in st_label:
        today_cls = "today-cell-green"
        badge_html = f"<span class='badge-green'>{st_label}</span>"
    elif "🟡" in st_label:
        today_cls = "today-cell-yellow"
        badge_html = f"<span class='badge-yellow'>{st_label}</span>"
    else:
        today_cls = "today-cell-red"
        badge_html = f"<span class='badge-red'>{st_label}</span>"

    html_rows.append(
        f"<tr>"
        f"<td><span class='platform-pill'>{r['平台']}</span></td>"
        f"<td style='font-weight:600;color:#f8fafc;'>{r['核心指標']}</td>"
        f"<td class='num-col' style='color:#94a3b8;'>{r['10/15']}</td>"
        f"<td class='num-col' style='color:#cbd5e1;'>{r['10/22 首映']}</td>"
        f"<td class='num-col' style='color:#cbd5e1;'>{r['10/23']}</td>"
        f"<td class='num-col {today_cls}'>{r['10/24 今日']}</td>"
        f"<td class='center-col'>{badge_html}</td>"
        f"<td style='color:#cbd5e1;'>{r['關鍵數字與判讀']}</td>"
        f"</tr>"
    )

heatmap_html = (
    "<div class='table-scroll'>"
    "<table class='heatmap-table'>"
    "<thead><tr>"
    "<th>平台</th><th>核心指標</th><th class='num-col'>10/15</th><th class='num-col'>10/22 首映</th><th class='num-col'>10/23</th><th class='num-col'>10/24 今日最新</th><th class='center-col'>狀態燈號</th><th>關鍵數字與趨勢判讀</th>"
    "</tr></thead>"
    "<tbody>" + "".join(html_rows) + "</tbody></table></div>"
)
st.markdown(heatmap_html, unsafe_allow_html=True)

# ==============================================================================
# SECTION 2: 📈 總趨勢折線圖 & 🥧 圓餅占比
# ==============================================================================
st.markdown("""
<div class="section-header">
    <h2 class="section-title">📈 2. 總趨勢折線圖與 🥧 全網聲量圓餅占比</h2>
    <p class="section-subtitle">左圖追蹤 Google Trends 每日熱度與《消失的她》黃金交叉走勢；右圖呈現全網累積總聲量從 7.6 萬攀升至 26.4 萬的成長斜率</p>
</div>
""", unsafe_allow_html=True)

CHART_FONT = dict(family="Inter, Noto Sans TC, sans-serif", size=13, color="#cbd5e1")
GRID_COLOR = "rgba(148, 163, 184, 0.12)"

col_line1, col_line2 = st.columns(2, gap="large")

with col_line1:
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
        title=dict(text="Google Trends 每日搜尋熱度趨勢與黃金交叉對照 (9/24–10/24)", font=dict(size=16, color="#f8fafc")),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=CHART_FONT,
        xaxis=dict(showgrid=False, linecolor=GRID_COLOR),
        yaxis=dict(title="相對熱度 (0–100)", range=[-6, 114], gridcolor=GRID_COLOR, zeroline=False),
        height=420,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=24, r=24, t=80, b=24)
    )
    st.plotly_chart(fig_gt, use_container_width=True)

with col_line2:
    tb = data["total_buzz_trend"]
    fig_buzz = go.Figure()
    fig_buzz.add_trace(go.Scatter(
        x=tb["dates"], y=tb["total_buzz"],
        mode="lines+markers+text",
        name="全網累積總聲量 (觀看+曝光+互動)",
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.14)",
        line=dict(color="#10b981", width=4, shape="spline"),
        marker=dict(size=11, color="#10b981", line=dict(width=2, color="#090d16")),
        text=[f"{v:,}" for v in tb["total_buzz"]],
        textposition="top center",
        textfont=dict(size=13, color="#6ee7b7")
    ))
    fig_buzz.add_trace(go.Scatter(
        x=tb["dates"], y=tb["yt_long"],
        mode="lines+markers",
        name="官方 YouTube 長片總觀看 (6支)",
        line=dict(color="#38bdf8", width=3, dash="dash", shape="spline"),
        marker=dict(size=8, color="#38bdf8")
    ))
    fig_buzz.add_trace(go.Scatter(
        x=tb["dates"], y=tb["social_views_and_eng"],
        mode="lines+markers",
        name="Threads 瀏覽與社群互動合計",
        line=dict(color="#f59e0b", width=2.5, shape="spline"),
        marker=dict(size=7, color="#f59e0b")
    ))
    fig_buzz.update_layout(
        title=dict(text="全網總聲量跨日成長折線圖（10/24 單日 +6.2萬 / +30.8% 🟢）", font=dict(size=16, color="#f8fafc")),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=CHART_FONT,
        xaxis=dict(showgrid=False, linecolor=GRID_COLOR),
        yaxis=dict(title="累積聲量數值", range=[0, 310000], gridcolor=GRID_COLOR, zeroline=False),
        height=420,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=24, r=24, t=80, b=24)
    )
    st.plotly_chart(fig_buzz, use_container_width=True)

col_pie1, col_pie2 = st.columns(2, gap="large")

with col_pie1:
    df_pv = pd.DataFrame(data["pie_views"])
    fig_pv = px.pie(
        df_pv, names="name", values="value", hole=0.52,
        title="全網累積觀看與曝光來源占比（總計 258,910 次）",
        color_discrete_sequence=["#38bdf8", "#10b981", "#6366f1", "#f59e0b", "#ec4899", "#64748b"]
    )
    fig_pv.update_traces(
        textposition="inside", textinfo="percent",
        textfont=dict(size=13, color="#ffffff"),
        marker=dict(line=dict(color="#111827", width=2.5))
    )
    fig_pv.update_layout(
        title=dict(font=dict(size=16, color="#f8fafc")),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=CHART_FONT,
        height=390,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
        margin=dict(l=20, r=120, t=60, b=20),
        annotations=[dict(text="<b>25.9萬</b><br>總觀看曝光", x=0.5, y=0.5, font_size=14, showarrow=False, font_color="#f8fafc")]
    )
    st.plotly_chart(fig_pv, use_container_width=True)

with col_pie2:
    df_pe = pd.DataFrame(data["pie_engagement"])
    fig_pe = px.pie(
        df_pe, names="name", values="value", hole=0.52,
        title="社群自然討論與貼文實質互動占比（Threads 占 59.5% 主力）",
        color_discrete_sequence=["#10b981", "#f43f5e", "#3b82f6", "#f59e0b", "#a855f7", "#64748b"]
    )
    fig_pe.update_traces(
        textposition="inside", textinfo="percent",
        textfont=dict(size=13, color="#ffffff"),
        marker=dict(line=dict(color="#111827", width=2.5))
    )
    fig_pe.update_layout(
        title=dict(font=dict(size=16, color="#f8fafc")),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=CHART_FONT,
        height=390,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
        margin=dict(l=20, r=120, t=60, b=20),
        annotations=[dict(text="<b>2,526次</b><br>實質互動", x=0.5, y=0.5, font_size=14, showarrow=False, font_color="#f8fafc")]
    )
    st.plotly_chart(fig_pe, use_container_width=True)

# ==============================================================================
# SECTION 3: 🎓 Dcard 登入搜尋結果專區 & 💬 今日新抓到的 12 則 YouTube 評論視覺化
# ==============================================================================
st.markdown("""
<div class="section-header">
    <h2 class="section-title">🎓 3. Dcard 登入搜尋結果專區 ＆ 💬 今日新抓 12 則 YouTube 評論視覺化</h2>
    <p class="section-subtitle">左側為「金鳳娜」Chrome 設定檔登入 Dcard 實測的 2 篇特映文與 1 個話題標籤；右側為今日新擷取的 12 則 YouTube 觀眾評論話題結構與明細</p>
</div>
""", unsafe_allow_html=True)

col_dcard, col_ytc = st.columns([1.0, 1.35], gap="large")

with col_dcard:
    dc = data["dcard_details"]
    st.markdown(
        f"<div class='info-card' style='border-left: 4px solid #10b981;'>"
        f"<div class='info-card-title'>✅ Dcard 登入與搜尋狀態</div>"
        f"<div style='color:#cbd5e1;font-size:0.93rem;'>{dc['login_status']}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    tag = dc["topic_tag"]
    st.markdown(
        f"<div class='info-card' style='border-left: 4px solid #38bdf8;'>"
        f"<div class='info-card-title'>🏷️ 話題標籤（1 個）：<a href='{tag['url']}' target='_blank' style='color:#38bdf8;text-decoration:none;'>{tag['name']}</a></div>"
        f"<span class='metric-chip'>📄 收錄文章：{tag['posts']} 篇</span>"
        f"<span class='metric-chip'>👥 追蹤人數：{tag['followers']} 人</span>"
        f"<div style='margin-top:10px;color:#94a3b8;font-size:0.9rem;'>{tag['note']}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    for idx_p, p in enumerate(dc["posts"], 1):
        st.markdown(
            f"<div class='info-card'>"
            f"<div class='info-card-title'>📄 官方特映文 {idx_p}｜{p['board']}：<a href='{p['url']}' target='_blank' style='color:#38bdf8;text-decoration:none;'>{p['title']}</a></div>"
            f"<div style='color:#94a3b8;font-size:0.86rem;margin-bottom:8px;'>發文單位：{p['author']} ｜ 發布時間：{p['date']} ｜ 標籤：{' '.join(p['tags'])}</div>"
            f"<span class='metric-chip'>❤️ 愛心 {p['hearts']}</span>"
            f"<span class='metric-chip'>💬 留言 {p['comments']}</span>"
            f"<span class='metric-chip'>🔖 收藏 {p['bookmarks']}</span>"
            f"<span class='metric-chip'>🔗 分享 {p['shares']}</span>"
            f"<div style='margin-top:10px;color:#cbd5e1;font-size:0.92rem;'><b>留言區實測：</b>{p['comment_detail']}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        f"<div class='info-card' style='border-left: 4px solid #f59e0b;background-color:rgba(245, 158, 11, 0.06);'>"
        f"<div class='info-card-title' style='color:#fbbf24;'>🌪️ 為什麼 Dcard 尚無學生映後文？</div>"
        f"<div style='color:#e2e8f0;font-size:0.92rem;'>{dc['typhoon_note']}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

with col_ytc:
    df_ytc = pd.DataFrame(data["youtube_comments_12"])

    sub_c1, sub_c2 = st.columns(2, gap="medium")
    with sub_c1:
        cat_counts = df_ytc.groupby("情緒與話題分類", as_index=False).agg(
            則數=("編號", "count"),
            總按讚=("按讚數", "sum")
        ).sort_values("則數", ascending=True)
        fig_cat = px.bar(
            cat_counts, x="則數", y="情緒與話題分類", orientation="h",
            text="則數", color="情緒與話題分類",
            title="12 則評論話題分布（主題曲與懸疑期待居首）",
            color_discrete_sequence=["#6366f1", "#f59e0b", "#a855f7", "#38bdf8", "#10b981"]
        )
        fig_cat.update_traces(textposition="outside", marker_line_width=0)
        fig_cat.update_layout(
            title=dict(font=dict(size=14, color="#f8fafc")),
            paper_bgcolor="#111827", plot_bgcolor="#111827", font=CHART_FONT,
            xaxis=dict(range=[0, 5.2], showgrid=True, gridcolor=GRID_COLOR),
            yaxis=dict(title=""),
            height=270, showlegend=False, margin=dict(l=12, r=24, t=48, b=16)
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with sub_c2:
        vid_counts = df_ytc.groupby("所屬影片", as_index=False).agg(
            留言則數=("編號", "count"),
            累計按讚=("按讚數", "sum")
        )
        fig_vid = px.bar(
            vid_counts, x="所屬影片", y=["留言則數", "累計按讚"], barmode="group",
            title="各支預告與主題曲：留言則數 vs 累計按讚",
            color_discrete_sequence=["#38bdf8", "#10b981"]
        )
        fig_vid.update_layout(
            title=dict(font=dict(size=14, color="#f8fafc")),
            paper_bgcolor="#111827", plot_bgcolor="#111827", font=CHART_FONT,
            xaxis=dict(title="", showgrid=False),
            yaxis=dict(title="", gridcolor=GRID_COLOR),
            height=270,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=""),
            margin=dict(l=12, r=16, t=54, b=16)
        )
        st.plotly_chart(fig_vid, use_container_width=True)

    st.markdown("<div style='font-weight:700;color:#f8fafc;margin:4px 0 8px 0;font-size:0.98rem;'>💬 今日新擷取 12 則 YouTube 觀眾真實評論一覽表</div>", unsafe_allow_html=True)
    st.dataframe(
        df_ytc[["編號", "所屬影片", "留言者", "留言內容", "按讚數", "情緒與話題分類"]],
        use_container_width=True,
        hide_index=True,
        height=340
    )

if os.path.exists(WC_IMG_PATH):
    with st.expander("🖼️ 點擊展開：《消失的金鳳娜》12 則 YouTube 評論 × PTT 15 則推文 × Threads 熱門口碑文字雲", expanded=False):
        st.image(WC_IMG_PATH, use_container_width=True)

# ==============================================================================
# SECTION 4: 📋 全平台按日期成長量化總表
# ==============================================================================
st.markdown("""
<div class="section-header">
    <h2 class="section-title">📋 4. 全平台指標「按日期成長」完整量化總表（23 項核心指標）</h2>
    <p class="section-subtitle">涵蓋 Google Trends、YouTube 各支影片、Threads、Instagram、Facebook、Dcard、PTT、X 與新聞媒體的逐日數值對照</p>
</div>
""", unsafe_allow_html=True)

df_quant = pd.DataFrame(data["quantitative_full_table"])
platform_options = ["全部平台 (23項)"] + sorted(df_quant["平台"].unique().tolist())
selected_platform = st.selectbox("依平台篩選量化指標", platform_options)
if selected_platform != "全部平台 (23項)":
    df_quant_show = df_quant[df_quant["平台"] == selected_platform]
else:
    df_quant_show = df_quant

st.dataframe(df_quant_show, use_container_width=True, hide_index=True, height=450)

# ==============================================================================
# SECTION 5: 📂 細部數據備查（可折疊展開）
# ==============================================================================
st.markdown("""
<div class="section-header">
    <h2 class="section-title">📂 5. 細部數據備查（點擊展開查看 PTT 推文、表外新增新聞與官方 Shorts 明細）</h2>
    <p class="section-subtitle">平時收合保持版面清爽，需要核對單則推文或新聞連結時點擊即可展開</p>
</div>
""", unsafe_allow_html=True)

with st.expander("📌 展開查看：PTT movie 板全部 15 則推文完整明細（2 篇文章）", expanded=False):
    df_ptt = pd.DataFrame(data["ptt_pushes_15"])
    st.dataframe(df_ptt, use_container_width=True, hide_index=True)

with st.expander("📰 展開查看：不在官方整理表（153 則）內的 7 則新增新聞與專業影評", expanded=False):
    df_news = pd.DataFrame(data["extra_news_7"])
    st.dataframe(df_news, use_container_width=True, hide_index=True)

with st.expander("📱 展開查看：Threads 自然熱門貼文 Top 5 與官方 YouTube 11 支 Shorts 明細", expanded=False):
    st.markdown("""
    **Threads 搜尋「消失的金鳳娜」熱門（Top）前 5 則：**
    1. `@jingyu4603`（12 小時前，一般網友）：期待陳冲，稱這是自己 2026 最好奇的國片（**980 讚、35 留言、42 轉發、98 分享，共 1,155 互動**）
    2. `@kimier33`（20 小時前，一般網友）：談 A-Lin 主題曲《寶貝愛人》10/27 上架、電影 10/29 上映（**139 讚、3 留言、12 轉發、27 分享，共 181 互動**）
    3. `@lingohsieh`（導演謝庭菡，9/25）：轉貼官方預告（**83 讚、2 留言、8 轉發、63 分享**）
    4. `@hi_iam_littledream`（1 天前，一般網友）：好奇片名為何從《寶貝愛人》改成《消失的金鳳娜》（**17 讚、2 留言**）
    5. `@aniswodimaya`（1 天前，一般網友）：貼海報稱「絕無冷場」（**12 讚、2 留言、4 轉發**）

    **官方 YouTube Shorts（共 11 支，合計 17,982 次觀看）：**
    - 最高前四支：「天后的真面目」3,972 次、「信仰篇」2,778 次、「慈祥笑容的背後」2,222 次、「院長開示篇」1,955 次
    - 最新兩支：「上映倒數 6 天」1,100 次、「10/29 全台戲院見」955 次
    """)

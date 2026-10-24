# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="《消失的金鳳娜》THE EVIL INSIDE｜即時聲量戰情室",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dashboard_data.json")
ASSETS_DIR = os.path.join(BASE_DIR, "docs", "assets")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Noto+Sans+TC:wght@400;500;600;700;800&family=Noto+Serif+TC:wght@600;700;800&display=swap');

:root {
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
    --font-sans: 'Noto Sans TC', sans-serif;
    --font-serif: 'Noto Serif TC', serif;
    --font-mono: 'Fira Code', 'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--font-sans) !important;
    background-color: var(--bg-canvas) !important;
    color: var(--text-primary) !important;
    font-variant-numeric: tabular-nums !important;
}

.block-container {
    max-width: 1400px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.cmd-header {
    background: rgba(16, 19, 28, 0.92);
    border: 1px solid var(--border-strong);
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
}
.cmd-title {
    font-family: var(--font-serif);
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text-primary);
}
.countdown-pill {
    background: rgba(225, 29, 72, 0.18);
    color: #FDA4AF;
    padding: 4px 12px;
    border-radius: 999px;
    font-family: var(--font-mono);
    font-size: 0.82rem;
    font-weight: 700;
    margin-left: 10px;
}
.bento-grid {
    display: grid;
    grid-template-columns: 1.35fr repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.bento-hero {
    grid-row: span 2;
    background: linear-gradient(150deg, #131724 0%, #191222 65%, #23111E 100%);
    border: 1px solid var(--border-strong);
    border-radius: 14px;
    padding: 24px;
}
.hero-big-num {
    font-family: var(--font-mono);
    font-size: 2.6rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.15;
}
.bento-card {
    background: var(--surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 18px 20px;
}
.card-label {
    font-size: 0.86rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 6px;
}
.card-val {
    font-family: var(--font-mono);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.card-delta {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: #6EE7B7;
    font-weight: 600;
}
.sec-head {
    margin-top: 28px;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-subtle);
}
.sec-title {
    font-family: var(--font-serif);
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}
@media (max-width: 1024px) {
    .bento-grid { grid-template-columns: 1fr; }
    .bento-hero { grid-row: span 1; }
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="cmd-header">
    <div>
        <span class="cmd-title">🎬 《消失的金鳳娜》THE EVIL INSIDE｜即時聲量戰情室</span>
        <span class="countdown-pill">距離 10/29 全台上映倒數 4 天｜今日 16:00 高雄電影節特映</span>
    </div>
    <div style="font-size:0.85rem;color:#94A3B8;">最後同步：{data['last_updated']}</div>
</div>

<div class="bento-grid">
    <div class="bento-hero">
        <div style="font-family:var(--font-mono);font-size:0.78rem;color:#FCD34D;margin-bottom:6px;">CROSS-PLATFORM TOTAL BUZZ &amp; REACH</div>
        <div style="font-size:1.25rem;font-weight:800;margin-bottom:10px;">全網跨平台累計總觸及與互動聲量</div>
        <div class="hero-big-num">548,920</div>
        <div style="color:#6EE7B7;font-family:var(--font-mono);font-weight:700;margin:8px 0;">🟢 +67,272 (+14.0%) vs 昨日</div>
        <p style="font-size:0.9rem;color:#E2E8F0;line-height:1.65;">核心預告與社群擴散總聲量達 318,992（單日 +54,645 / +20.7%），加計 162 則新聞媒體與外部長短影音跨平台總觸及達 548,920 次。</p>
    </div>
    <div class="bento-card">
        <div class="card-label">YouTube 預告與花絮總觀看</div>
        <div class="card-val">244,876</div>
        <div class="card-delta">🟢 +46,668 (+23.5%)</div>
    </div>
    <div class="bento-card">
        <div class="card-label">FB 雙粉專與演員貼文互動量</div>
        <div class="card-val">279 粉 / 429 互動</div>
        <div class="card-delta">🟢 張翰 148 讚｜謝文憲 82 讚</div>
    </div>
    <div class="bento-card">
        <div class="card-label">IG 官方追蹤與 Reels 互動量</div>
        <div class="card-val">389 粉 / 820 互動</div>
        <div class="card-delta">🟢 +15 粉 (+4.0%)｜45 貼文</div>
    </div>
    <div class="bento-card">
        <div class="card-label">Threads @9wo0725 與脆友熱議</div>
        <div class="card-val">31.5K 瀏覽 / 4,531 互動</div>
        <div class="card-delta">🟢 單篇飆至 3,536 讚 (+261%)</div>
    </div>
    <div class="bento-card" style="grid-column: span 2;">
        <div class="card-label">媒體新聞與論壇（Dcard / PTT / Google Trends）擴散</div>
        <div class="card-val">162 則新聞 ｜ PTT 15 推 ｜ Trends 熱度 97 (連3日滿檔)</div>
        <div class="card-delta">🟢 雙片搜尋對照 51 : 43 連 4 日領先《消失的她》｜今日 16:00 高雄電影節特映</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-head"><h2 class="sec-title">1. 🟢🟡🔴 跨平台聲量成長熱力矩陣</h2></div>', unsafe_allow_html=True)
df_hm = pd.DataFrame(data["heatmap_rows"])
st.dataframe(df_hm, use_container_width=True, hide_index=True)

st.markdown('<div class="sec-head"><h2 class="sec-title">2. 最新短影音與行銷素材展示區（NEWS LIVE 獨家新聞爆料風 v1）</h2></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.image(os.path.join(ASSETS_DIR, "cover_a_9x16.webp"), caption="款式 A (9:16 直式)")
    st.markdown("[▶ 觀看/下載 9:16 款式 A MP4](https://drive.google.com/file/d/1gpp0uBBS9kqRLQhHjx5uvmMxV_QyuqoK/view?usp=sharing)")
with c2:
    st.image(os.path.join(ASSETS_DIR, "cover_b_9x16.webp"), caption="款式 B (9:16 直式)")
    st.markdown("[▶ 觀看/下載 9:16 款式 B MP4](https://drive.google.com/file/d/1plgDG-aAn8Am3M6lpceTXQ2bwa3W1R8Q/view?usp=sharing)")
with c3:
    st.image(os.path.join(ASSETS_DIR, "cover_a_16x9.webp"), caption="款式 A (16:9 橫式)")
    st.markdown("[▶ 觀看/下載 16:9 款式 A MP4](https://drive.google.com/file/d/1fvBn-32WJpHyQYmySBG-2Kpa4k9aGr4T/view?usp=sharing)")
with c4:
    st.image(os.path.join(ASSETS_DIR, "cover_b_16x9.webp"), caption="款式 B (16:9 橫式)")
    st.markdown("[▶ 觀看/下載 16:9 款式 B MP4](https://drive.google.com/file/d/1arsM8Kpfnez_zpRE2u6OqBHEorONHoLV/view?usp=sharing)")

st.markdown('<div class="sec-head"><h2 class="sec-title">3. 全平台 23 項指標與真實評論檢索庫</h2></div>', unsafe_allow_html=True)
df_quant = pd.DataFrame(data["quantitative_full_table"])
st.dataframe(df_quant, use_container_width=True, hide_index=True)

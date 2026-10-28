# 🎬 《消失的金鳳娜》THE EVIL INSIDE｜Muse AI「`Amo02`」專責：即時聲量戰情室每日自動爬文與數據更新指令包（核定版）

- **制定與交辦日期**：2026-10-28（Asia/Taipei, UTC+8｜上映倒數 D-1）
- **專責執行帳號**：**Muse AI 的 `Amo02`**（`Amo_a02`）
- **督導與驗收中樞**：Grok Bot · 總幕僚長（配合本機 0-Token 雙軌同步引擎 `/workspace/jinfengna_dashboard/sync_jinfengna_live.py` 與 GitHub Actions 自動編譯流水線）
- **即時聲量戰情室線上網址**：`https://kp20240001-netizen.github.io/jinfengna-buzz-dashboard/`
- **首映 24h 口碑牆線上網址**：`https://kp20240001-netizen.github.io/jinfengna-buzz-dashboard/premiere_24h_reviews.html`
- **GitHub 儲存庫（Repo）**：`https://github.com/kp20240001-netizen/jinfengna-buzz-dashboard`（分支：`main`）
- **Google Drive 專責派工與回報資料夾（已開通 `anyoneWithLink: writer` 任何人可檢視與編輯寫入）**：
  - 🔗 **專責資料夾連結**：`https://drive.google.com/drive/folders/1C9nNJco7XmBeKnJlhenlWYpGs9x8eHoW`（Folder ID：`1C9nNJco7XmBeKnJlhenlWYpGs9x8eHoW`）

---

## 一、核心問題解答：「戰情室頁面權限是否讓 `Amo02` 串接 GitHub 即可？」

**✅ 結論：是的！直接讓 `Amo02` 串接 GitHub 即可，而且我們已為您升級好「GitHub Actions 自動編譯 ＋ Google Drive 免權限雙向橋接」雙保險機制：**

| 更新路徑 | 權限配置方式 | `Amo02` 需執行的動作 | 後端自動編譯與上線機制（已部署完成） |
| :--- | :--- | :--- | :--- |
| **模式 A（首推・最快）<br>GitHub 直連更新法** | 在 Muse AI (`Amo02`) 綁定 GitHub Connector，或提供僅限 `kp20240001-netizen/jinfengna-buzz-dashboard` 單一 Repo 之 `Contents: Read & Write` Fine-grained Token | `Amo02` 每日爬完 7 大平台數據後，**只需直接修改並 Commit/Push 根目錄的 `dashboard_data.json`（及首映後的 `premiere_reviews_data.json`）**，完全不必手動改 HTML/JS！ | Repo 已部署 **`.github/workflows/auto-build-pages.yml`**：只要偵測到 `dashboard_data.json` 或 `premiere_reviews_data.json` 更新，GitHub Actions 會在 20 秒內自動執行 `export_static_site.py` 與 `update_premiere_reviews.py`，自動重新編譯 `docs/index.html`、`docs/dashboard.js` 與 `docs/premiere_24h_reviews.html` 並發布至 GitHub Pages！ |
| **模式 B（零風險備援）<br>Google Drive 寫回更新法** | **免設定任何 GitHub 權限**（直接使用已開通 `anyoneWithLink: writer` 的 Google Drive 專責資料夾） | `Amo02` 每日將更新後的 `dashboard_data.json`（或 `YYYY-MM-DD_Amo02_金鳳娜聲量數據.json`）與 `YYYY-MM-DD_Amo02執行報告.md` 寫回本 Google Drive 專責資料夾 | 本機每 30 分鐘執行的 0-Token 排程 **`/workspace/jinfengna_dashboard/sync_jinfengna_live.py`** 會自動掃描 Google Drive 專責資料夾（`1C9nNJco7XmBeKnJlhenlWYpGs9x8eHoW`），一旦發現新上傳的 JSON 立即自動拉取、通過紅線與 Schema 驗證後編譯 `docs/` 並 `git push` 更新戰情室！ |

> 💡 **強制規定**：無論 `Amo02` 採用模式 A（GitHub 直連）或模式 B（Google Drive 寫回）更新數據，**每日執行完畢後都必須將 `YYYY-MM-DD_Amo02執行報告.md` 寫回同一個 Google Drive 專責資料夾**，供總幕僚長（Grok Bot）讀取並向使用者（yang）作三行回報！

---

## 二、每日固定自動爬文範圍：7 大平台監測清單與核心指標

請 `Amo02` 設定 **每日固定 1 次自動排程（建議每日早上 `08:00` 或 `08:30` Asia/Taipei UTC+8）**，巡檢以下 7 大平台並更新數據：

### 1. YouTube（官方長片 6 支 ＋ 官方 Shorts 12+ 支 ＋ 導演頻道 ＋ 林知夏主題曲 MV ＋ 外部媒體）
- **① 官方頻道 `@Dasun_Pictures`（大算影業）**：
  - 頻道訂閱數、影片總數。
  - **6 支核心長片觀看數、按讚數、留言數與新增觀眾留言**：
    1. 《花絮：地獄爬回來的女人》(`10/15` 上傳)
    2. 《30秒預告》
    3. 《電影預告｜10/29 全台上映》(`https://www.youtube.com/watch?v=TYUTLbbhUJ8`)
    4. 《真實故事改編 正式預告》(`https://www.youtube.com/watch?v=Cu7JRGIbJaY`)
    5. 《A-Lin【寶貝愛人】主題曲 Teaser》(`https://www.youtube.com/watch?v=lCdDkrZ-3c4`)
    6. 《花絮：人命標的166號》(`10/21` 上傳)
  - **官方 Shorts 短影音合計（目前 12 支＋後續倒數與映後新增 Shorts）**：統計總支數、合計觀看數、合計按讚數。
- **② 導演謝庭菡自有頻道《抓馬人生不打碼》（`https://www.youtube.com/@rawdramalife`）**：
  - ⚠️ **【永久嚴格過濾鐵律】**：該頻道為綜合型 Podcast 頻道，**嚴格只篩選標題或內容含 `(消失的金鳳娜|金鳳娜|喜翔|陳冲|陳沖|劉奕兒|陽靚|張翰|謝庭菡)` 之電影宣傳長片與 Shorts**（如 `71LivMoJnAA`、`kOC41eQsv7A`、`CF-1yJs5gUA` 及新上架宣傳片），**絕不混入頻道內其他無關影片觀看數**！
- **③ 林知夏 Livia Lin 主題曲深情翻唱版 MV**：
  - 影片網址：`https://youtu.be/R-YA2Ss_YE8`（Video ID: `R-YA2Ss_YE8`，《寶貝愛人（林知夏版）｜電影《消失的金鳳娜》主題曲 MV》，`10/29 20:00` 首播）
  - 追蹤指標：觀看次數、按讚數、留言數與高讚觀眾催淚留言。
- **④ 外部媒體與創作者 YouTube 專訪／預告**：
  - 北市影委會預告 (`w7IseDHJvA4`)、中廣《欸！我說到哪裡了》(`Ucr2h7ENLsM`)、POP Radio《POP最正點》(`-4H5DngqlR8`)、TVBS 新聞 (`f_iDJ19L96A`)、WhatA VOGUE 首映 QA (`P2A4QWDV-s0`)、Linda 影評等合計觀看數。

### 2. Google Trends（台灣區搜尋熱度）
- 「消失的金鳳娜」單獨搜尋熱度（0–100 指標與六都縣市熱區分布）。
- 雙片對照搜尋比：「消失的金鳳娜」vs「消失的她」跨日趨勢比值與飆升搜尋詞（如：陳冲、A-Lin、寶貝愛人、買命黑幕）。

### 3. Threads（自然討論熱門串文 ＋ 官方與投資方帳號）
- 搜尋關鍵字「消失的金鳳娜」、「金鳳娜」之熱門脆友串文（追蹤如 `@jingyu4603`、`@kimier33`、`@hulk740813` 及每日新增映後口碑串文之按讚、留言、轉發、分享數）。
- 專案投資方日記帳號 `@9wo0725`：追蹤者數、串文總數、累計瀏覽數與最新串文互動。
- 官方 Threads 帳號 `@theevilinsidemovie`：追蹤者數、串文數與最高讚貼文表現。

### 4. Instagram（`@theevilinsidemovie`）
- 官方 IG 帳號追蹤者人數、貼文總數、Reels 與貼文累積互動數（按讚＋留言＋分享）。

### 5. Facebook（官方粉專 ＋ 藝人名人擴散貼文）
- 官方粉專粉絲數、「正在談論這個」人數。
- 藝人與名人貼文擴散互動（如張翰、謝文憲、周曉涵、劉奕兒、陽靚、喜翔等貼文按讚與分享總互動）。

### 6. Dcard ＆ PTT movie 板（外加 X / Twitter）
- **PTT `movie` 板**：搜尋「金鳳娜」之文章篇數、累積推文數（推／→／噓）與新增 `[好雷]`、`[普雷]` 映後心得文明細（寫入 `ptt_pushes_15` 與 `premiere_reviews_data.json`）。
- **Dcard 電影板與 `#消失的金鳳娜` 話題頁**：收錄文章數、愛心數、留言數與學生特映場映後心得。
- **X (Twitter)**：關鍵字貼文數、總曝光數與按讚數。

### 7. 新聞媒體報導與全台戲院場次／首映口碑
- Google News 搜尋「消失的金鳳娜」最新媒體報導篇數與表外新增重要影評／新聞標題與連結（寫入 `extra_news_7`）。
- `10/29` 上映後：每日同步收集最新影評金句、觀眾無雷好評與全台戲院場次熱度，一併更新 `premiere_reviews_data.json`。

---

## 三、絕對紅線與防破版鐵律（Anti-Jobs & Red Lines）

1. **🚫 女主角姓名唯一紅線**：全片唯一正確女主角名稱為 **「金鳳娜」**，任何數據、摘要、評論與報告**絕對禁止誤植為「林月鳳」或「林春鳳」**！
2. **🚫 禁用四字詞紅線**：全站 JSON 與報告**嚴禁出現「「死亡・賭局」（禁用四字詞）」四字**（請一律使用「買命黑幕」、「地下賭王買命黑幕」或「166號買命標的」替代；本機與 GitHub Actions 設有 `verify_redline` 自動攔截）。
3. **🚫 JSON 結構零破版鐵律**：更新 `dashboard_data.json` 與 `premiere_reviews_data.json` 時，必須 100% 保持與同資料夾內 `02_dashboard_data_schema_and_template.json`、`03_premiere_reviews_data_template.json` 相同的頂層 Key 名稱與陣列物件結構，確保前端圖表（Plotly）與熱力矩陣零破版。

---

## 四、可直接複製貼給 Muse AI「`Amo02`」的完整派工 Prompt

> 📋 **請直接複製下方整段指令，貼給 Muse AI 的 `Amo02` 對話視窗啟動每日自動排程任務**：

```text
【Muse AI `Amo02` 常駐專責任務：《消失的金鳳娜》THE EVIL INSIDE 即時聲量戰情室 — 每日自動爬文、數據更新與雲端回報】

你是《消失的金鳳娜》（THE EVIL INSIDE）即時聲量戰情室的專責數據工程與情報官 `Amo02`。
請立即建立並執行「每日固定 1 次（每日早上 08:30 Asia/Taipei UTC+8）」的跨平台聲量自動爬文與戰情室更新排程。

### 📁 一、關鍵資源與權限位置
1. **即時聲量戰情室前端網址**：https://kp20240001-netizen.github.io/jinfengna-buzz-dashboard/
2. **首映 24h 口碑牆網址**：https://kp20240001-netizen.github.io/jinfengna-buzz-dashboard/premiere_24h_reviews.html
3. **GitHub 儲存庫（Repo）**：https://github.com/kp20240001-netizen/jinfengna-buzz-dashboard （分支：`main`）
4. **Google Drive 專責派工與回報共用資料夾（已開通 `anyoneWithLink: writer` 可直接讀寫）**：
   👉 https://drive.google.com/drive/folders/1C9nNJco7XmBeKnJlhenlWYpGs9x8eHoW （Folder ID: `1C9nNJco7XmBeKnJlhenlWYpGs9x8eHoW`）
   - 資料夾內已附標準欄位範本：`02_dashboard_data_schema_and_template.json` 與 `03_premiere_reviews_data_template.json`。

### 🔍 二、每日自動爬文範圍（7 大平台）
每日請自動巡檢並抓取以下 7 大平台之最新真實數據（嚴禁捏造未驗證數據）：
1. **YouTube**：
   - 官方頻道 `@Dasun_Pictures`：6 支長片觀看數/按讚/留言（地獄爬回來的女人花絮、30秒預告、電影預告 `TYUTLbbhUJ8`、正式預告 `Cu7JRGIbJaY`、A-Lin 寶貝愛人 Teaser `lCdDkrZ-3c4`、人命標的166號花絮）＋ 官方 Shorts 短影音總觀看與總讚數。
   - 導演謝庭菡頻道 `@rawdramalife`（`https://www.youtube.com/@rawdramalife`）：【嚴格過濾】只統計標題含 `(消失的金鳳娜|金鳳娜|喜翔|陳冲|陳沖|劉奕兒|陽靚|張翰|謝庭菡)` 之宣傳片（如 `71LivMoJnAA`、`kOC41eQsv7A`、`CF-1yJs5gUA` 及新增本片宣傳片），絕不混入頻道其他無關影片！
   - 林知夏主題曲 MV：`https://youtu.be/R-YA2Ss_YE8`（《寶貝愛人》林知夏版，追蹤觀看數、按讚數與熱門留言）。
   - 外部媒體 YouTube 影片（中廣、POP Radio、TVBS、北市影委會、WhatA VOGUE 等）合計觀看。
2. **Google Trends（台灣）**：「消失的金鳳娜」單獨熱度（0–100）、六都熱區分數，以及「消失的金鳳娜 vs 消失的她」雙片對照比值。
3. **Threads**：搜尋「消失的金鳳娜」自然熱門串文總互動（按讚/留言/轉發/分享）、`@9wo0725` 投資方日記瀏覽與串文數、`@theevilinsidemovie` 官方追蹤與互動。
4. **Instagram**：`@theevilinsidemovie` 官方追蹤人數、貼文數與累積互動。
5. **Facebook**：官方粉專粉絲數、正在談論人數，以及藝人名人（張翰、謝文憲、周曉涵等）推薦貼文互動數。
6. **PTT movie 板 / Dcard / X**：PTT movie 板討論篇數與最新推文（更新至 `ptt_pushes_15`）、Dcard `#消失的金鳳娜` 話題頁與電影板篇數/愛心/留言、X 貼文曝光數。
7. **新聞媒體與映後口碑**：最新媒體報導總則數與新增新聞明細（更新至 `extra_news_7`），並將最新影評與觀眾無雷口碑同步更新至 `premiere_reviews_data.json`。

### 🔄 三、戰情室數據更新步驟（支援 GitHub 直連 ＆ Google Drive 雙軌自動同步）
請依 `02_dashboard_data_schema_and_template.json` 的 JSON 欄位格式更新數據（注意：全篇嚴禁誤植「林月鳳／林春鳳」，且嚴禁出現「「死亡・賭局」（禁用四字詞）」四字，請用「買命黑幕」替代）：
- **方式 A（GitHub 直連更新）**：直接將更新後的 `dashboard_data.json`（與 `premiere_reviews_data.json`）Commit 並 Push 至 GitHub Repo `kp20240001-netizen/jinfengna-buzz-dashboard` 的 `main` 分支。GitHub Actions（`auto-build-pages.yml`）會自動執行 Python 編譯 `docs/index.html` 與 `docs/dashboard.js` 並即時發布上線！
- **方式 B（Google Drive 寫回更新）**：若未透過 GitHub Push，請直接將更新後的 `dashboard_data.json`（或命名為 `YYYY-MM-DD_Amo02_金鳳娜聲量數據.json`）上傳至上述 Google Drive 專責資料夾（`1C9nNJco7XmBeKnJlhenlWYpGs9x8eHoW`），本機排程 `sync_jinfengna_live.py` 會自動拉取、編譯並推送至 GitHub Pages。

### 📝 四、【強制規定】每日寫回 Markdown 執行報告至同一個 Google Drive 資料夾
每次完成每日爬文與數據更新後，**必須將當日執行報告直接寫入／上傳至同一個 Google Drive 專責資料夾**：
👉 https://drive.google.com/drive/folders/1C9nNJco7XmBeKnJlhenlWYpGs9x8eHoW
- **強制檔名格式**：`YYYY-MM-DD_Amo02執行報告.md`（例如：`2026-10-28_Amo02執行報告.md`）。
- **報告內容必須包含以下三行摘要結構（供總幕僚長 Grok Bot 直接讀取回報）**：
  1. **① 成品路徑／更新狀態**：列出當日已更新之 GitHub Commit 或 Google Drive JSON 檔名、執行報告連結與戰情室最後同步時間戳。
  2. **② 做了什麼（7 大平台今日聲量亮點）**：摘要今日全網累計總觸及與核心聲量總數、較昨日增幅（+Δ / +Δ%），以及 YouTube（含官方長片/Shorts、導演頻道、`R-YA2Ss_YE8` 林知夏主題曲）、Threads、IG/FB、Dcard/PTT、新聞媒體之關鍵變化。
  3. **③ 有無問題**：確認欄位 Schema 是否 100% 驗證通過、戰情室網頁是否正常渲染（HTTP 200）、有無異常或待辦事項。
```

#!/usr/bin/env python3
"""
《消失的金鳳娜》跨平台聲量戰情室 — 本機零 Token 雙軌自動拉取（GitHub + Google Drive Amo02 專責夾）與靜態頁面編譯同步腳本
檔案：/workspace/jinfengna_dashboard/sync_jinfengna_live.py
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import urllib.request

BASE_DIR = "/workspace/jinfengna_dashboard"
DATA_PATH = os.path.join(BASE_DIR, "dashboard_data.json")
REVIEWS_DATA_PATH = os.path.join(BASE_DIR, "premiere_reviews_data.json")
EXPORT_SCRIPT = os.path.join(BASE_DIR, "export_static_site.py")
UPDATE_REVIEWS_SCRIPT = os.path.join(BASE_DIR, "update_premiere_reviews.py")
AMO02_HANDOFF_DIR = os.path.join(BASE_DIR, "amo02_handoff_pack")
DRIVE_SYNC_STATE_PATH = os.path.join(AMO02_HANDOFF_DIR, ".drive_sync_state.json")

# Google Drive Folder ID: Muse_Amo02_消失的金鳳娜_即時聲量戰情室每日爬文與更新專責包
AMO02_DRIVE_FOLDER_ID = "1C9nNJco7XmBeKnJlhenlWYpGs9x8eHoW"

TZ_TAIPEI = datetime.timezone(datetime.timedelta(hours=8))
RELEASE_DATE = datetime.date(2026, 10, 29)
FORBIDDEN_REDLINE = "死亡" + "賭局"


def now_taipei():
    return datetime.datetime.now(TZ_TAIPEI)


def verify_redline_and_schema(raw_text: str, is_reviews: bool = False) -> dict:
    if FORBIDDEN_REDLINE in raw_text:
        raise ValueError("RED LINE VIOLATION: Forbidden 4-character phrase detected!")
    for wrong_name in ("林月鳳", "林春鳳"):
        if wrong_name in raw_text:
            raise ValueError(f"RED LINE VIOLATION: Wrong heroine name {wrong_name} detected!")
    parsed = json.loads(raw_text)
    if is_reviews:
        req_keys = ("movie_title", "hero_stats", "critic_and_celebrity_quotes", "audience_24h_wall", "theaters_and_ticketing")
    else:
        req_keys = ("kpi_cards", "heatmap_rows", "trends_daily", "total_buzz_trend", "pie_views", "quantitative_full_table")
    for k in req_keys:
        if k not in parsed:
            raise ValueError(f"Missing required schema key: {k}")
    return parsed


def pull_github_latest():
    """Track A: Pull latest commits from GitHub origin/main if Amo02 pushed directly."""
    subprocess.run(
        ["git", "-C", BASE_DIR, "pull", "--rebase", "--autostash", "origin", "main"],
        check=False,
        capture_output=True,
        text=True,
    )


def sync_from_amo02_google_drive() -> list:
    """
    Track B: Zero-Token check of Amo02 Google Drive shared folder (1C9nNJco7XmBeKnJlhenlWYpGs9x8eHoW).
    Detects newly uploaded dashboard_data.json, YYYY-MM-DD_Amo02_金鳳娜聲量數據.json,
    premiere_reviews_data.json, or YYYY-MM-DD_Amo02執行報告.md.
    """
    os.makedirs(AMO02_HANDOFF_DIR, exist_ok=True)
    state = {}
    if os.path.exists(DRIVE_SYNC_STATE_PATH):
        try:
            with open(DRIVE_SYNC_STATE_PATH, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {}

    synced_files = []
    list_url = f"https://drive.google.com/embeddedfolderview?id={AMO02_DRIVE_FOLDER_ID}#list"
    try:
        req = urllib.request.Request(list_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[WARN] Could not query Google Drive folder {AMO02_DRIVE_FOLDER_ID}: {e}")
        return synced_files

    pattern = re.compile(
        r'id="entry-([A-Za-z0-9_-]+)".*?<div class="flip-entry-title">([^<]+)</div>.*?<div class="flip-entry-last-modified"><div>([^<]+)</div>',
        re.S,
    )
    entries = pattern.findall(html)
    if not entries:
        return synced_files

    for file_id, title, mod_str in entries:
        title = title.strip()
        mod_str = mod_str.strip()
        state_key = f"{file_id}:{mod_str}"

        # Skip our own static template files in the handoff folder
        if title.startswith(("01_", "02_", "03_", "04_")):
            continue

        is_dashboard_json = (
            title == "dashboard_data.json"
            or ("Amo02" in title and title.endswith(".json") and "數據" in title)
            or (title.endswith("_dashboard_data.json"))
        )
        is_reviews_json = title == "premiere_reviews_data.json" or title.endswith("_premiere_reviews_data.json")
        is_report_md = ("Amo02執行報告" in title or "Amo02_執行報告" in title) and title.endswith(".md")

        if not (is_dashboard_json or is_reviews_json or is_report_md):
            continue

        if state.get(file_id) == state_key:
            continue

        dl_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        try:
            dl_req = urllib.request.Request(dl_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(dl_req, timeout=20) as dl_resp:
                raw_bytes = dl_resp.read()
            raw_text = raw_bytes.decode("utf-8")

            if is_dashboard_json:
                parsed = verify_redline_and_schema(raw_text, is_reviews=False)
                with open(DATA_PATH, "w", encoding="utf-8") as f:
                    json.dump(parsed, f, ensure_ascii=False, indent=2)
                synced_files.append(f"dashboard_data.json (from Drive: {title})")
            elif is_reviews_json:
                parsed = verify_redline_and_schema(raw_text, is_reviews=True)
                with open(REVIEWS_DATA_PATH, "w", encoding="utf-8") as f:
                    json.dump(parsed, f, ensure_ascii=False, indent=2)
                synced_files.append(f"premiere_reviews_data.json (from Drive: {title})")
            elif is_report_md:
                report_local_path = os.path.join(AMO02_HANDOFF_DIR, title)
                with open(report_local_path, "w", encoding="utf-8") as f:
                    f.write(raw_text)
                synced_files.append(f"report:{title}")

            state[file_id] = state_key
        except Exception as e:
            print(f"[WARN] Failed to process Drive file {title} ({file_id}): {e}")

    try:
        with open(DRIVE_SYNC_STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    return synced_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(DATA_PATH):
        return

    # 1. Track A: Pull latest from GitHub (in case Amo02 updated via GitHub directly)
    pull_github_latest()

    # 2. Track B: Check Amo02 Google Drive shared folder for new JSON/Report uploads
    drive_synced = sync_from_amo02_google_drive()

    now = now_taipei()
    countdown = max(0, (RELEASE_DATE - now.date()).days)
    ts_str = f"{now.strftime('%Y-%m-%d %H:%M')} (台北時間 UTC+8｜上映倒數 {countdown} 天)"

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["last_updated"] = ts_str
    data["countdown_days"] = countdown

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    subprocess.run(["/usr/bin/python3", EXPORT_SCRIPT], cwd=BASE_DIR, check=True)
    subprocess.run(["/usr/bin/python3", UPDATE_REVIEWS_SCRIPT], cwd=BASE_DIR, check=True)

    if args.push:
        files_to_stage = [
            "dashboard_data.json",
            "premiere_reviews_data.json",
            "docs/index.html",
            "docs/dashboard.js",
            "docs/premiere_24h_reviews.html",
            "premiere_24h_reviews.html",
        ]
        subprocess.run(["git", "-C", BASE_DIR, "add"] + files_to_stage, check=False)
        st = subprocess.run(
            ["git", "-C", BASE_DIR, "status", "--porcelain"] + files_to_stage,
            capture_output=True,
            text=True,
        )
        if st.stdout.strip():
            src_note = f" + Drive sync ({', '.join(drive_synced)})" if drive_synced else ""
            commit_msg = f"chore(war-room): auto-sync timestamp, countdown & static pages ({now.strftime('%Y-%m-%d %H:%M')} UTC+8){src_note}"
            subprocess.run(["git", "-C", BASE_DIR, "commit", "-m", commit_msg], check=False)
            subprocess.run(["git", "-C", BASE_DIR, "pull", "--rebase", "origin", "main"], check=False)
            subprocess.run(["git", "-C", BASE_DIR, "push", "origin", "main"], check=False)


if __name__ == "__main__":
    main()

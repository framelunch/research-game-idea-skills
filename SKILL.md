---
name: research-game-skills
description: Research niche game ideas for small indie teams (1–3 people) targeting mobile apps and Steam. Investigates Reddit pain points, Hacker News discussions, and Qiita articles (Japanese market) to surface underserved opportunities. Use this skill whenever someone wants to find game ideas, discover market gaps, research what games are missing, explore indie game opportunities, or identify what players are asking for. Also trigger when someone mentions "穴場のゲーム", "ゲームアイデア調査", "インディーゲーム市場", or similar Japanese phrases about game research.
---

# Niche Game Idea Research for Small Indie Teams

You are a game market researcher helping a small team (1–3 developers) find underserved, high-potential game ideas for **mobile apps** and **Steam**.

## Step 1: Confirm the Research Year

Before doing anything else, ask the user in Japanese:

> **「調査対象の年号を教えてください（例：2024年）。」**

Wait for their answer. Use `{year}` throughout the research.

**Date range logic (handled automatically by the scripts):**
- **Past year** (e.g. 2024 when current year is 2026): uses the full calendar year, Jan 1 – Dec 31.
- **Current year** (e.g. 2026 when current year is 2026): the year hasn't finished, so the scripts use a **rolling 12-month window** — from exactly one year ago to today. This ensures a full year of data even when the calendar year is partial.

## Step 2: Research Sources

Run research across three sources in parallel using the provided scripts. Detailed search strategies are in the references directory — read them before proceeding.

### Reddit pain points
Run `scripts/fetch_reddit.py` to collect game-related Reddit posts:

```bash
python scripts/fetch_reddit.py --year {year} --output /tmp/reddit_raw.json
```

Then read `/tmp/reddit_raw.json` and extract the top pain points. See `references/reddit-research.md` for guidance on interpreting the results.

### Hacker News popular posts
Run `scripts/fetch_hn.py` to collect game-related HN posts:

```bash
python scripts/fetch_hn.py --year {year} --output /tmp/hn_raw.json
```

Then read `/tmp/hn_raw.json` and extract the high-engagement posts. See `references/hackernews-research.md` for guidance on interpreting the results.

### Qiita articles（日本語市場）
Run `scripts/fetch_qiita.py` to collect game-related Qiita articles.

Load the QIITA_TOKEN from `.env` to enable authenticated access (higher rate limits), then run the script:

```bash
QIITA_TOKEN=$(grep '^QIITA_TOKEN=' .env | cut -d= -f2) \
  python scripts/fetch_qiita.py --year {year} --output /tmp/qiita_raw.json
```

Then read `/tmp/qiita_raw.json` and extract high-engagement articles. See `references/qiita-research.md` for guidance on interpreting the results. Qiita is especially valuable for understanding the **Japanese domestic market** — individual developer release reports, unmet needs in Japanese, and Japan-specific opportunities.

Don't fabricate findings — if the scripts return no useful data, say so.

## Step 3: Synthesize Game Ideas

From your research, identify **3–5 niche game ideas** that:
- Address a pain point or unmet desire expressed by real users
- Are feasible for a team of 1–3 developers
- Have a plausible path to revenue on mobile or Steam (or both)

For each idea, provide a structured report using the format in `references/output-template.md`.

Evaluate each idea using the 5-point framework defined in `references/evaluation-framework.md`.

## Step 4: Save and Present Results

Save the full report as a markdown file to:
```
<skill_directory>/report/{year}/{YYYY-MM-DD}/report_{HHmmss}.md
```

Where:
- `<skill_directory>` is the directory containing this SKILL.md file
- `{year}` is the research target year (e.g. `2024`)
- `{YYYY-MM-DD}` is today's date (the date the research was conducted, e.g. `2026-03-10`)
- `{HHmmss}` is the current time when the research is conducted (e.g. `143022`)

The filename is `report_{HHmmss}.md`, so multiple runs on the same day are saved as separate files.

Create directories as needed.

Then present a summary in the chat in **Japanese**. Include a brief summary table at the top listing all ideas with their overall scores, then provide full detail on each.

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/reddit-research.md` | Which subreddits to search, what to look for, how to extract pain points |
| `references/hackernews-research.md` | How to find game-related HN posts with high engagement |
| `references/qiita-research.md` | How to find game-related Qiita articles and extract Japanese market signals |
| `references/evaluation-framework.md` | 5-point scoring rubric for each evaluation dimension |
| `references/output-template.md` | Exact output format for each game idea |

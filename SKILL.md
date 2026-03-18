---
name: research-game-skills
description: Research niche game ideas for small indie teams (1–3 people) targeting mobile apps and Steam. Investigates Reddit pain points, Hacker News discussions, Qiita articles (Japanese market), and Indie Hackers founder discussions to surface underserved opportunities and growing niche markets. Use this skill whenever someone wants to find game ideas, discover market gaps, research what games are missing, explore indie game opportunities, identify growing niches, or identify what players are asking for. Also trigger when someone mentions "穴場のゲーム", "ゲームアイデア調査", "インディーゲーム市場", "成長中のニッチ市場", or similar Japanese phrases about game research.
---

# Niche Game Idea Research for Small Indie Teams

You are a game market researcher helping a small team (1–3 developers) find underserved, high-potential game ideas for **mobile apps** and **Steam**.

## Step 1: Confirm Research Parameters

Before doing anything else, ask the user **three questions in a single message** in Japanese:

> **「以下の3点を教えてください。**
>
> **① 調査対象の年号（例：2024年）**
>
> **② 興味のあるゲームジャンル（例：アクション、対戦・PvP、コージーゲーム、ノベル・ADV、パズル、ローグライク、シミュレーション、RPG、その他）**
> 　複数選択可。「指定なし」なら全ジャンルを対象にします。
>
> **③ ターゲット市場（国内（日本）／海外（グローバル）／両方）」**

Wait for their answers. Use `{year}`, `{genre_filter}`, and `{market_focus}` throughout the research.

## Step 2: Research Sources

Run all four scripts in parallel. After each script completes, read its output file and consult the corresponding reference file for interpretation guidance.

### Reddit pain points

```bash
python scripts/fetch_reddit.py --year {year} --output /tmp/reddit_raw.json
```

Read `/tmp/reddit_raw.json`. See `references/reddit-research.md`.

### Hacker News popular posts

```bash
python scripts/fetch_hn.py --year {year} --output /tmp/hn_raw.json
```

Read `/tmp/hn_raw.json`. See `references/hackernews-research.md`.

### Qiita articles（日本語市場）

```bash
QIITA_TOKEN=$(grep '^QIITA_TOKEN=' .env | cut -d= -f2) \
  python scripts/fetch_qiita.py --year {year} --output /tmp/qiita_raw.json
```

Read `/tmp/qiita_raw.json`. See `references/qiita-research.md`.

### Indie Hackers growing niches

Indie Hackers はAPIもHTMLスクレイピングも利用不可のため、WebSearch で直接調査する。`references/indiehackers-research.md` に記載されたクエリを使って WebSearch を実行し、結果を解釈する。

Don't fabricate findings — if a script returns no useful data, say so.

## Step 3: Synthesize Game Ideas

From your research, identify **3–5 niche game ideas**.

Apply source weighting and filters as described in `references/source-weighting.md`.
Score each idea using `references/evaluation-framework.md`.
Format each idea using `references/output-template.md`.

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

The report must begin with the following metadata section:

```markdown
## 実行メタデータ

- **実行日時**: {YYYY-MM-DD HH:mm:ss}
- **スキル**: research-game-skills
- **与えたプロンプト**:
  ```
  {the exact args/prompt passed to this skill via the Skill tool}
  ```
- **調査パラメータ**:
  - 対象年号: {year}
  - ジャンル: {genre_filter}
  - 市場: {market_focus}
```

Then present a summary in the chat in **Japanese**. Include a brief summary table at the top listing all ideas with their overall scores, then provide full detail on each.

## Step 5: Post-Execution Review

After presenting the results, review the skill itself for issues encountered during this run:

1. **Script errors or warnings** — did any script fail, time out, or return unexpectedly empty results? If so, investigate the cause and fix the script.
2. **Data quality issues** — were the results too thin, off-topic, or missing key signals? Consider adjusting queries, keywords, or filters in the relevant script or reference file.
3. **Documentation gaps** — does any reference file (`references/*.md`) contradict the actual script behavior (e.g., missing queries, wrong options)? Fix the discrepancy.
4. **README updates** — if scripts or behavior changed, update `README.md` to reflect the current state.

Apply fixes directly. Only mention issues to the user if a fix requires their input (e.g., missing API token, intentional behavior change).

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/source-weighting.md` | How to weight sources by market focus, apply genre/growth filters, and handle date ranges |
| `references/reddit-research.md` | Which subreddits to search, what to look for, how to extract pain points |
| `references/hackernews-research.md` | How to find game-related HN posts with high engagement |
| `references/qiita-research.md` | How to find game-related Qiita articles and extract Japanese market signals |
| `references/indiehackers-research.md` | How to find growing niche market signals and revenue-validated ideas on Indie Hackers |
| `references/evaluation-framework.md` | Idea selection criteria + 5-point scoring rubric |
| `references/output-template.md` | Exact output format for each game idea |

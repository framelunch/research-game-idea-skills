# Qiita Research Guide

## Goal

Qiita is Japan's largest technical knowledge-sharing platform for programmers. Individual developers and indie game creators frequently post about their development experiences, market observations, and release reports — making it a valuable source for understanding **Japanese domestic market trends and unmet needs in the Japanese-speaking market**.

## Why Qiita for Game Research

Qiita readers and contributors are primarily Japanese-speaking engineers. It surfaces:

- **Individual developer game release reports** (raw accounts including sales numbers, download counts, and struggles)
- **"I wish this game existed" / "I'm frustrated with existing games" articles**
- **Unity / Godot / Unreal implementation logs** (what was hard = signals entry barriers)
- **Ground-level feel for the domestic indie game market** (Japan-specific demand that overseas research misses)

Articles with high like counts (50+) indicate that many developers or players share the same concern.

## Search Strategies

### Qiita API (primary)

Use `scripts/fetch_qiita.py` to auto-fetch. The API is accessible without authentication (60 req/hour).

```bash
python scripts/fetch_qiita.py --year {year} --output /tmp/qiita_raw.json
```

Default queries and their intent:

| Query | Target |
|-------|--------|
| `インディーゲーム` | Domestic indie games in general |
| `ゲーム開発` | Developer firsthand experiences and struggles |
| `Unity ゲーム` | Release logs for Unity-based games |
| `Godot ゲーム` | Personal projects using lightweight engines |
| `モバイルゲーム 個人開発` | Mobile × solo dev intersection |
| `Steam ゲーム 個人` | Personal game release experiences on Steam |
| `個人開発 ゲーム リリース` | Reports including sales / download figures |
| `ゲームアイデア` | Unimplemented ideas and feature requests |
| `ゲーム 穴場` | Direct mentions of untapped niches |
| `ゲーム 市場調査` | Market analysis articles |
| `hyper casual game` | English-mixed articles on casual games |
| `casual game 個人` | Firsthand solo casual game dev experiences |

### Qiita Web Search (supplementary)

If the script returns thin results, supplement with WebSearch / WebFetch:

```
site:qiita.com ゲーム 個人開発 {year}
site:qiita.com インディーゲーム リリース {year}
site:qiita.com "個人開発" "ゲーム" "売上"
```

## What Signals to Extract

For each article, note:

1. **Like count (`likes_count`)** — 30+ is notable; 100+ signals high demand
2. **Comment count** — many questions and discussion means many developers share the same pain
3. **Specific numbers** — download counts, revenue, playtime data that indicate market size
4. **"I struggled because X didn't exist" / "I wished there was Y"** — direct expressions of unmet needs
5. **Tags** — `Unity`, `Godot`, `iOS`, `Android`, `Steam`, etc. reveal target platforms

## Patterns That Signal Opportunity

- **"Reached X downloads as a solo dev" articles** — treat as real market data for genre + platform
- **"Game Y has no Japanese localization"** — signals translation / localization demand
- **Articles where many comments say "I had the same problem"** — confirms a shared pain point
- **"This is standard overseas but doesn't exist in Japan" lament articles** — signals import opportunity
- **Low-like articles with unusually specific numbers** — rare primary data worth keeping

## Red Flags

- Articles that are purely technical implementation notes with no market or user perspective
- Topics referencing outdated engine / framework versions (stale needs)
- "I made this" posts with no mention of release, reception, or downloads

## Output

List the top 5–8 Qiita articles with title, like count, comment count, and URL. Add a one-line market signal summary for each. Pass the strongest signals to the synthesis step.

# Hacker News Research Guide

## Goal

Find game-related posts on Hacker News that generated strong community engagement. HN skews technical and indie-leaning — it's a good signal for games that appeal to developers, early adopters, and thoughtful players who will also leave detailed feedback.

## Why HN for Game Research

HN readers often discuss:
- Indie games that punched above their weight commercially
- "Show HN" posts from solo/small-team developers with community reactions
- Games with novel mechanics that attracted attention
- Market opportunities that technical readers have noticed

High comment counts on HN (50+) indicate genuine interest, not just virality.

## Search Strategies

### HN Search (primary)
Use `https://hn.algolia.com/` via WebFetch or WebSearch:

```
site:news.ycombinator.com game {year}
site:news.ycombinator.com "Show HN" game {year}
site:news.ycombinator.com indie game {year}
```

Direct Algolia API searches (fetch these URLs):
```
https://hn.algolia.com/api/v1/search?query=indie+game&tags=story&numericFilters=created_at_i>={year_unix_start},created_at_i<={year_unix_end}&hitsPerPage=20
```

For `{year}` = 2024:
- `year_unix_start` = 1704067200
- `year_unix_end` = 1735689599

Adjust for other years accordingly (Jan 1 00:00 UTC to Dec 31 23:59 UTC).

### What to Search For

```
"Show HN" game
"Show HN" indie
"Show HN" mobile game
small team game
solo developer game
game released {year}
game launched {year}
```

## What Signals to Extract

For each HN post, note:

1. **Points (upvotes)** — 100+ is strong, 300+ is exceptional
2. **Comment count** — 50+ comments indicates real discussion
3. **Comment sentiment** — are people saying "I'd pay for this" or "we need more like this"?
4. **"Ask HN" threads** — look for "Ask HN: what game would you like to see made?" type posts
5. **Team size mentions** — prioritize solo or small-team projects that did well

## Patterns That Signal Opportunity

- **High-point "Show HN" games in niche categories** — if a tiny team's game got 500 points, the genre has an engaged audience
- **Comment threads asking "is there a mobile version?"** — signals demand on a different platform
- **Posts where commenters list competing games that all have major flaws** — the niche is real but unsatisfied
- **Games praised for "doing one thing really well"** — these succeed because they fill a focused gap

## Red Flags

- Posts where top comments are about technical implementation, not the game itself (developer interest, not player interest)
- Games that succeeded primarily due to HN novelty effect (e.g., trivial browser toys)
- Categories where established players (Valve, Nintendo, etc.) clearly dominate

## Output

Compile a list of 5–8 HN posts with titles, point counts, comment counts, and your read on what market signal each one provides. Include the HN post URL for reference. Pass the strongest signals to the synthesis step.

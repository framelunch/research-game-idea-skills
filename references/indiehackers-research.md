# Indie Hackers Research Guide

## Goal

Find game-related discussions, product launches, and revenue data from Indie Hackers to surface **growing niche markets** and validated business opportunities for small indie game teams.

## Why Indie Hackers for Game Research

IH is where indie developers share **actual revenue numbers, growth trajectories, and lessons learned**. Unlike Reddit (player complaints) or HN (technical discussion), IH provides:

- Real MRR/ARR data from indie game developers
- Founder interviews on what worked and what didn't
- Early signals of **emerging niches** before they hit mainstream coverage
- Discussion threads where developers openly compare markets and monetization strategies

High vote counts on IH (20+) indicate the topic resonates with practitioners, not just observers.

## Search Strategies

### Group Posts (primary)
Game-relevant IH groups to check:
- `/group/gaming` — general game developer discussion
- `/group/mobile-apps` — mobile game developers
- `/group/games` — product and launch discussions
- `/group/indie-games` — indie-specific conversations

### Post Feed Search
Search for game-related posts in the global feed:
```
game, indie game, mobile game, steam, puzzle, roguelike,
cozy game, idle game, hypercasual, niche game, growing market
```

### Products
Search IH products with queries:
```
game, mobile game, indie game, puzzle, roguelike, idle, casual
```

The product database includes MRR estimates and maker counts — useful for validating whether a game category is generating real revenue.

## What Signals to Extract

For each IH post or product, note:

1. **Votes and comment count** — 20+ votes is strong engagement from practitioners
2. **Revenue mentions** — "$X MRR", "reached $X/month", "crossed $X ARR" indicate proven monetization
3. **Growth trajectory language** — "growing fast", "unexpected audience", "niche I didn't expect"
4. **Market gap statements** — "nobody was doing X", "I searched and couldn't find a game that..."
5. **Platform mentions** — which platform (mobile, Steam, browser) is seeing growth in underserved areas
6. **Team size** — solo founders or 2-person teams who hit traction are high-signal for small-team viability

## Patterns That Signal Growing Niche Markets

- **Founder reports faster-than-expected growth in an unusual genre** — strong signal the niche is heating up
- **Multiple founders independently mentioning the same underserved market** — consensus signal
- **"I built this for myself and it blew up"** — indicates latent demand that wasn't being served
- **Game categories where founders report high revenue with minimal marketing** — the market pulls organically
- **Cross-platform success of a niche concept** — e.g., a PC game ported to mobile finding a new audience

## Red Flags

- Posts where revenue is attributed entirely to a one-time viral moment (e.g., a single YouTuber video)
- Products with no MRR data and vague claims about "thousands of users"
- Niches where all recent IH posts show declining interest or failed launches
- Games built for Western markets with no obvious path to global monetization (if `{market_focus}` = 国内)

## Interpreting `ih_raw.json`

The script output contains two collections:

- **`posts`** — IH forum posts sorted by engagement score (`votes + comments × 2`). Focus on posts with `votes ≥ 10` for strong signals.
- **`products`** — IH product listings for game-related products. Check `mrr` and `maker_count` to identify categories with solo/small-team success.

When `{genre_filter}` is specified, filter posts and products by matching the genre keywords against `title`, `body_snippet`, and `tags`.

## Output

Compile a list of 5–8 IH posts or products with titles, vote counts, and your read on what market signal each one provides. For products, include any revenue data. Pass the strongest "growing niche" signals to the synthesis step.

#!/usr/bin/env python3
"""
fetch_hn.py - Fetch game-related posts from Hacker News via Algolia Search API.

Usage:
    python scripts/fetch_hn.py --year 2025 --output /tmp/hn_raw.json
    python scripts/fetch_hn.py --year 2025 --min-points 5 --output /tmp/hn_raw.json

HN Algolia API is public and requires no authentication.
"""

import argparse
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone


# Query terms relevant to indie games on HN
GAME_QUERIES = [
    "indie game",
    "Show HN game",
    "Show HN indie",
    "Show HN mobile game",
    "small team game",
    "solo developer game",
    "game released",
    "game launched",
    "mobile game",
    "steam game",
    "puzzle game",
    "roguelike",
    "cozy game",
    "idle game",
    "browser game",
]

ALGOLIA_BASE = "https://hn.algolia.com/api/v1/search"

# Keywords that confirm a post is game-related (title must match at least one)
GAME_RELATED_KEYWORDS = [
    "game", "gaming", "indie", "steam", "mobile game", "puzzle", "roguelike",
    "rpg", "cozy", "idle", "browser game", "gamedev", "game dev", "unity",
    "godot", "unreal", "playthrough", "player", "gameplay",
]


def is_game_related(title: str) -> bool:
    """Return True if the post title is clearly game-related."""
    title_lower = title.lower()
    return any(kw in title_lower for kw in GAME_RELATED_KEYWORDS)


def date_range_for_year(year: int) -> tuple[int, int]:
    """Return (start_unix, end_unix) for the target year.

    If year == current year (i.e. the year hasn't finished), use a rolling
    12-month window ending today instead of Jan 1 – Dec 31. This ensures we
    capture a full year's worth of data even when the calendar year is partial.
    """
    now = datetime.now(timezone.utc)
    if year >= now.year:
        # Rolling window: exactly 1 year back from today
        one_year_ago = now.replace(year=now.year - 1)
        return int(one_year_ago.timestamp()), int(now.timestamp())
    else:
        # Completed calendar year
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        return int(start.timestamp()), int(end.timestamp())


def fetch_hn_posts(query: str, year: int, min_points: int = 5) -> list[dict]:
    """Fetch HN posts matching a query within the given year."""
    # Build date range for the year
    year_start, year_end = date_range_for_year(year)

    params = urllib.parse.urlencode({
        "query": query,
        "tags": "story",
        "numericFilters": f"created_at_i>{year_start},created_at_i<{year_end},points>={min_points}",
        "hitsPerPage": 20,
    })
    url = f"{ALGOLIA_BASE}?{params}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GameIdeaResearch/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("hits", [])
    except Exception as e:
        print(f"  Warning: HN query '{query}' failed: {e}")
        return []


def normalize_post(hit: dict, query: str) -> dict:
    """Normalize an Algolia HN hit to a standard structure."""
    return {
        "object_id": hit.get("objectID", ""),
        "title": hit.get("title", ""),
        "url": hit.get("url", ""),
        "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
        "points": hit.get("points", 0),
        "num_comments": hit.get("num_comments", 0),
        "author": hit.get("author", ""),
        "created_at": hit.get("created_at", ""),
        "matched_query": query,
        "engagement_score": hit.get("points", 0) + hit.get("num_comments", 0) * 2,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch game-related HN posts for idea research")
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year for filtering posts (default: current year)")
    parser.add_argument("--min-points", type=int, default=5,
                        help="Minimum HN points threshold (default: 5)")
    parser.add_argument("--output", type=str, default="/tmp/hn_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--queries", type=str, default=None,
                        help="Comma-separated query list (default: built-in game list)")
    args = parser.parse_args()

    queries = args.queries.split(",") if args.queries else GAME_QUERIES
    target_year = args.year

    print(f"Fetching HN posts for year {target_year} using {len(queries)} queries...")

    seen_ids = set()
    all_posts = []

    for query in queries:
        print(f"  Searching: '{query}'...")
        hits = fetch_hn_posts(query, target_year, min_points=args.min_points)

        for hit in hits:
            post = normalize_post(hit, query)
            # Skip posts that are clearly unrelated to games
            if not is_game_related(post["title"]):
                continue
            if post["object_id"] not in seen_ids:
                seen_ids.add(post["object_id"])
                all_posts.append(post)

        time.sleep(0.5)  # gentle rate limiting

    # Sort by engagement
    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(all_posts),
        "queries_used": queries,
        "posts": all_posts,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Found {len(all_posts)} unique HN posts.")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()

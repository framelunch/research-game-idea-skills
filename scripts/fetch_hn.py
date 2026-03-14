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


def fetch_hn_posts(query: str, year: int, min_points: int = 5) -> list[dict]:
    """Fetch HN posts matching a query within the given year."""
    # Build date range for the year
    year_start = int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp())
    year_end = int(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp())

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

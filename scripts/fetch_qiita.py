#!/usr/bin/env python3
"""
fetch_qiita.py - Fetch game-related articles from Qiita via the Qiita API v2.

Usage:
    python scripts/fetch_qiita.py --year 2025 --output /tmp/qiita_raw.json
    python scripts/fetch_qiita.py --year 2025 --min-likes 5 --output /tmp/qiita_raw.json

Qiita API v2 is public and supports unauthenticated access (60 req/hour).
For higher rate limits, set QIITA_TOKEN environment variable.
"""

import argparse
import json
import os
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone


# Query terms relevant to indie games on Qiita (Japanese tech blog)
GAME_QUERIES = [
    "インディーゲーム",
    "ゲーム開発",
    "Unity ゲーム",
    "Godot ゲーム",
    "モバイルゲーム 個人開発",
    "Steam ゲーム 個人",
    "ゲームアイデア",
    "個人開発 ゲーム リリース",
    "ゲーム 穴場",
    "ゲーム 市場調査",
    "hyper casual game",
    "casual game 個人",
]

QIITA_BASE = "https://qiita.com/api/v2/items"

# Keywords that confirm an article is game-related (title or tags must match at least one)
GAME_RELATED_KEYWORDS = [
    "ゲーム", "game", "unity", "unreal", "godot", "インディー", "indie",
    "steam", "モバイルゲーム", "アプリゲーム", "ゲーム開発", "gamedev",
    "rpg", "パズル", "puzzle", "アクション", "シミュレーション",
    "ローグライク", "roguelike", "カジュアルゲーム", "ゲームデザイン",
]


def is_game_related(title: str, tags: list[str]) -> bool:
    """Return True if the article is clearly game-related."""
    haystack = title.lower() + " " + " ".join(t.lower() for t in tags)
    return any(kw in haystack for kw in GAME_RELATED_KEYWORDS)


def date_range_for_year(year: int) -> tuple[str, str]:
    """Return (start_date_str, end_date_str) for the target year.

    If year == current year (i.e. the year hasn't finished), use a rolling
    12-month window ending today instead of Jan 1 – Dec 31.
    """
    from datetime import date, timedelta
    today = date.today()
    if year >= today.year:
        start = today.replace(year=today.year - 1)
        return start.isoformat(), today.isoformat()
    else:
        return f"{year}-01-01", f"{year}-12-31"


def fetch_qiita_articles(query: str, year: int, min_likes: int = 1, token: str = None) -> list[dict]:
    """Fetch Qiita articles matching a query within the given year."""
    start_date, end_date = date_range_for_year(year)
    date_filter = f"created:>={start_date} created:<={end_date}"
    full_query = f"{query} {date_filter}"

    params = urllib.parse.urlencode({
        "query": full_query,
        "per_page": 20,
        "page": 1,
    })
    url = f"{QIITA_BASE}?{params}"

    headers = {"User-Agent": "GameIdeaResearch/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            items = json.loads(response.read().decode("utf-8"))
            return [item for item in items if item.get("likes_count", 0) >= min_likes]
    except Exception as e:
        print(f"  Warning: Qiita query '{query}' failed: {e}")
        return []


def normalize_article(item: dict, query: str) -> dict:
    """Normalize a Qiita API item to a standard structure."""
    return {
        "id": item.get("id", ""),
        "title": item.get("title", ""),
        "url": item.get("url", ""),
        "likes_count": item.get("likes_count", 0),
        "comments_count": item.get("comments_count", 0),
        "page_views_count": item.get("page_views_count") or 0,
        "author": item.get("user", {}).get("id", ""),
        "created_at": item.get("created_at", ""),
        "tags": [tag.get("name", "") for tag in item.get("tags", [])],
        "matched_query": query,
        "engagement_score": item.get("likes_count", 0) + item.get("comments_count", 0) * 3,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch game-related Qiita articles for idea research")
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year for filtering articles (default: current year)")
    parser.add_argument("--min-likes", type=int, default=1,
                        help="Minimum Qiita likes threshold (default: 1)")
    parser.add_argument("--output", type=str, default="/tmp/qiita_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--queries", type=str, default=None,
                        help="Comma-separated query list (default: built-in game list)")
    args = parser.parse_args()

    token = os.environ.get("QIITA_TOKEN")
    if token:
        print("Using QIITA_TOKEN for authenticated access (higher rate limits).")
    else:
        print("No QIITA_TOKEN set — using unauthenticated access (60 req/hour).")

    queries = args.queries.split(",") if args.queries else GAME_QUERIES
    target_year = args.year

    print(f"Fetching Qiita articles for year {target_year} using {len(queries)} queries...")

    seen_ids = set()
    all_articles = []

    for query in queries:
        print(f"  Searching: '{query}'...")
        items = fetch_qiita_articles(query, target_year, min_likes=args.min_likes, token=token)

        for item in items:
            article = normalize_article(item, query)
            # Skip articles that are clearly unrelated to games
            if not is_game_related(article["title"], article["tags"]):
                continue
            if article["id"] not in seen_ids:
                seen_ids.add(article["id"])
                all_articles.append(article)

        time.sleep(1.0)  # gentle rate limiting (unauthenticated: 60 req/hour)

    # Sort by engagement
    all_articles.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_articles": len(all_articles),
        "queries_used": queries,
        "articles": all_articles,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Found {len(all_articles)} unique Qiita articles.")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()

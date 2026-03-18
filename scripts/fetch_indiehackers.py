#!/usr/bin/env python3
"""
fetch_indiehackers.py - Fetch game-related posts and products from Indie Hackers.

Usage:
    python scripts/fetch_indiehackers.py --year 2025 --output /tmp/ih_raw.json
    python scripts/fetch_indiehackers.py --year 2025 --min-votes 5 --output /tmp/ih_raw.json

Indie Hackers has a public REST-like API backed by Firebase. No authentication required.
"""

import argparse
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone

IH_API_BASE = "https://www.indiehackers.com/api"

# Game-related group slugs on Indie Hackers
GAME_GROUPS = [
    "gaming",
    "mobile-apps",
    "games",
    "indie-games",
    "game-development",
]

# Fallback: search queries for the post endpoint
GAME_QUERIES = [
    "game",
    "indie game",
    "mobile game",
    "steam game",
    "puzzle game",
    "roguelike",
    "cozy game",
    "game development",
    "gaming",
    "idle game",
    "hypercasual",
    "niche game",
    "growing market",
    "underserved market",
]

GAME_RELATED_KEYWORDS = [
    "game", "gaming", "indie", "steam", "mobile game", "puzzle", "roguelike",
    "rpg", "cozy", "idle", "browser game", "gamedev", "game dev", "unity",
    "godot", "unreal", "player", "gameplay", "app store", "google play",
    "niche", "hypercasual", "casual game",
]


def is_game_related(text: str) -> bool:
    text_lower = text.lower()
    return any(kw in text_lower for kw in GAME_RELATED_KEYWORDS)


def date_range_for_year(year: int) -> tuple[int, int]:
    """Return (start_unix_ms, end_unix_ms) for the target year.

    Uses a rolling 12-month window when year == current year.
    """
    now = datetime.now(timezone.utc)
    if year >= now.year:
        try:
            one_year_ago = now.replace(year=now.year - 1)
        except ValueError:
            one_year_ago = now.replace(year=now.year - 1, day=28)
        return int(one_year_ago.timestamp() * 1000), int(now.timestamp() * 1000)
    else:
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        return int(start.timestamp() * 1000), int(end.timestamp() * 1000)


def fetch_url(url: str) -> dict | list | None:
    """Fetch a URL and return parsed JSON, or None on failure."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "GameIdeaResearch/1.0",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"  Warning: fetch failed for {url}: {e}")
        return None


def fetch_group_posts(group_slug: str, limit: int = 20) -> list[dict]:
    """Fetch top posts from a specific IH group."""
    url = f"{IH_API_BASE}/get-posts?groupSlug={group_slug}&filter=top&limit={limit}"
    data = fetch_url(url)
    if not data:
        return []
    # API returns a list or dict with 'posts' key
    if isinstance(data, list):
        return data
    return data.get("posts", [])


def fetch_top_posts(limit: int = 50) -> list[dict]:
    """Fetch top posts from the IH global feed."""
    url = f"{IH_API_BASE}/get-posts?filter=top&limit={limit}"
    data = fetch_url(url)
    if not data:
        return []
    if isinstance(data, list):
        return data
    return data.get("posts", [])


def fetch_products(query: str = "game", limit: int = 20) -> list[dict]:
    """Fetch IH products matching a query keyword."""
    params = urllib.parse.urlencode({"query": query, "limit": limit})
    url = f"{IH_API_BASE}/search-products?{params}"
    data = fetch_url(url)
    if not data:
        return []
    if isinstance(data, list):
        return data
    return data.get("products", [])


def normalize_post(raw: dict) -> dict:
    """Normalize an IH post to a standard structure."""
    created_at_raw = raw.get("createdAt") or raw.get("created_at") or 0
    # IH timestamps may be in ms or seconds
    if isinstance(created_at_raw, (int, float)) and created_at_raw > 1e10:
        created_at_raw = created_at_raw / 1000
    return {
        "id": raw.get("id", raw.get("slug", "")),
        "title": raw.get("title", ""),
        "body_snippet": (raw.get("body", "") or "")[:200],
        "url": f"https://www.indiehackers.com/post/{raw.get('slug', raw.get('id', ''))}",
        "votes": raw.get("votes", raw.get("upvoteCount", 0)),
        "comments": raw.get("commentCount", raw.get("comments", 0)),
        "author": raw.get("userId", raw.get("author", "")),
        "created_at": datetime.utcfromtimestamp(created_at_raw).isoformat() if created_at_raw else "",
        "created_at_unix": int(created_at_raw),
        "group": raw.get("groupSlug", ""),
        "engagement_score": (raw.get("votes", raw.get("upvoteCount", 0)) or 0)
                           + (raw.get("commentCount", raw.get("comments", 0)) or 0) * 2,
    }


def normalize_product(raw: dict) -> dict:
    """Normalize an IH product to a standard structure."""
    return {
        "id": raw.get("id", raw.get("slug", "")),
        "name": raw.get("name", ""),
        "tagline": raw.get("tagline", ""),
        "url": f"https://www.indiehackers.com/product/{raw.get('slug', raw.get('id', ''))}",
        "revenue": raw.get("revenueType", ""),
        "mrr": raw.get("revenue", {}).get("mrr", 0) if isinstance(raw.get("revenue"), dict) else 0,
        "maker_count": raw.get("makerCount", 1),
        "upvotes": raw.get("upvoteCount", 0),
        "tags": raw.get("tags", []),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch game-related Indie Hackers data for idea research")
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year for filtering posts (default: current year)")
    parser.add_argument("--min-votes", type=int, default=3,
                        help="Minimum votes threshold for posts (default: 3)")
    parser.add_argument("--output", type=str, default="/tmp/ih_raw.json",
                        help="Output JSON file path")
    args = parser.parse_args()

    start_ms, end_ms = date_range_for_year(args.year)
    start_sec = start_ms / 1000
    end_sec = end_ms / 1000

    print(f"Fetching Indie Hackers data for year {args.year}...")

    seen_ids = set()
    all_posts = []
    all_products = []

    # --- Fetch group posts ---
    for group_slug in GAME_GROUPS:
        print(f"  Group: '{group_slug}'...")
        raw_posts = fetch_group_posts(group_slug, limit=30)
        for raw in raw_posts:
            post = normalize_post(raw)
            if post["id"] in seen_ids:
                continue
            if post["votes"] < args.min_votes:
                continue
            if post["created_at_unix"] and not (start_sec <= post["created_at_unix"] <= end_sec):
                continue
            if not is_game_related(post["title"] + " " + post["body_snippet"]):
                continue
            seen_ids.add(post["id"])
            all_posts.append(post)
        time.sleep(0.5)

    # --- Fetch global top posts and filter game-related ---
    print("  Global top posts...")
    global_posts = fetch_top_posts(limit=100)
    for raw in global_posts:
        post = normalize_post(raw)
        if post["id"] in seen_ids:
            continue
        if post["votes"] < args.min_votes:
            continue
        if post["created_at_unix"] and not (start_sec <= post["created_at_unix"] <= end_sec):
            continue
        if not is_game_related(post["title"] + " " + post["body_snippet"]):
            continue
        seen_ids.add(post["id"])
        all_posts.append(post)
    time.sleep(0.5)

    # --- Fetch game-related products ---
    print("  Products (game-related)...")
    for query in ["game", "mobile game", "indie game", "puzzle", "roguelike"]:
        raw_products = fetch_products(query=query, limit=20)
        for raw in raw_products:
            product = normalize_product(raw)
            pid = product["id"]
            if pid and pid not in seen_ids:
                if is_game_related(product["name"] + " " + product["tagline"]):
                    seen_ids.add(pid)
                    all_products.append(product)
        time.sleep(0.5)

    # Sort by engagement
    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": args.year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(all_posts),
        "total_products": len(all_products),
        "posts": all_posts,
        "products": all_products,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Found {len(all_posts)} posts and {len(all_products)} products.")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()

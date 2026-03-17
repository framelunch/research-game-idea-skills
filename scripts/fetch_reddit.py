#!/usr/bin/env python3
"""
fetch_reddit.py - Fetch posts from game-related subreddits using Reddit's public JSON API.

Usage:
    python scripts/fetch_reddit.py --year 2025 --output /tmp/reddit_raw.json
    python scripts/fetch_reddit.py --year 2025 --limit 50 --output /tmp/reddit_raw.json

No authentication required (uses Reddit's public JSON API).
"""

import argparse
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone


GAME_SUBREDDITS = [
    # Primary (high signal)
    "patientgamers",
    "indiegaming",
    "indiegames",
    "gamedev",
    "SteamDeals",
    "iosgaming",
    "AndroidGaming",
    "SteamDeck",
    # Secondary (additional context)
    "truegaming",
    "gaming",
    "SuggestAGame",
    "tipofmyjoystick",
    "gamedesign",
    "solodev",
    "IndieDev",
    "WebGames",
    "cozygames",
]

# Phrases that signal a player pain point or unmet desire.
# Use multi-word phrases where possible to avoid false positives.
# Avoid bare single words like "wish" (matches "wishlists"), "need", "help", "want"
# which appear in unrelated developer milestone posts (e.g. r/solodev wishlist updates).
PAIN_SIGNAL_KEYWORDS = [
    # Direct "game doesn't exist" signals
    "i wish there was a game", "wish there was a game",
    "why isn't there a game", "why is there no game",
    "nobody has made a game", "no one has made a game",
    "i can't find a game", "can't find a game",
    "doesn't exist", "does not exist",
    "no game that", "no game like",
    # Desire / request signals
    "would love a game", "dream game",
    "looking for a game", "suggest a game",
    "game request", "game recommendation",
    # Frustration signals
    "frustrated with", "i'm frustrated", "so frustrated",
    "underserved", "missing feature", "market gap",
    # Cozy/mobile-specific common requests
    "cozy game that", "mobile game that",
    "ios game that", "android game that",
    "i need a game", "i want a game",
    "i need a cozy", "i want a cozy",
    "looking for cozy", "looking for a cozy",
    # Premium / monetization frustration
    "premium game", "no gacha", "no ads game",
    "pay to win", "pay-to-win",
]

# Subreddits where every post is a game request by definition
PAIN_POINT_SUBREDDITS = {"SuggestAGame", "tipofmyjoystick"}

HEADERS = {
    "User-Agent": "GameIdeaResearch/1.0 (educational research tool)",
}


def fetch_subreddit_posts(subreddit: str, limit: int = 25, sort: str = "top",
                          target_year: int | None = None) -> list[dict]:
    """Fetch posts from a subreddit using Reddit's public JSON API.

    When target_year is the current year or next year, uses t=year (past 12 months).
    For past years, uses t=all and applies client-side year filtering — note that
    Reddit's public API only returns up to ~1000 top posts, so coverage of older
    years may be incomplete. Consider supplementing with Pushshift/Arctic Shift for
    historical research beyond ~2 years ago.
    """
    current_year = datetime.now(timezone.utc).year
    # Use t=year only when requesting recent data (current or previous year)
    time_filter = "year" if target_year is None or target_year >= current_year - 1 else "all"
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}&t={time_filter}"
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            posts = data.get("data", {}).get("children", [])
            return [p["data"] for p in posts]
    except Exception as e:
        print(f"  Warning: Failed to fetch r/{subreddit}: {e}")
        return []


def is_pain_point(post: dict) -> bool:
    """Heuristic: does this post signal a user pain point or unmet desire?

    Uses two detection strategies:
    1. Subreddit-based: posts in r/SuggestAGame and r/tipofmyjoystick are
       game requests by definition.
    2. Keyword-based: multi-word phrases in the title that signal unmet desire.
       Single-word keywords are intentionally avoided to prevent false positives
       (e.g., "wish" matching developer milestone posts about "wishlists").
    """
    if post.get("subreddit") in PAIN_POINT_SUBREDDITS:
        return True
    title = post.get("title", "").lower()
    flair = (post.get("link_flair_text") or "").lower()
    return any(kw in title or kw in flair for kw in PAIN_SIGNAL_KEYWORDS)


def date_range_for_year(year: int) -> tuple[float, float]:
    """Return (start_unix, end_unix) for the target year.

    If year == current year (i.e. the year hasn't finished), use a rolling
    12-month window ending now instead of Jan 1 – Dec 31.
    """
    now = datetime.now(timezone.utc)
    if year >= now.year:
        try:
            one_year_ago = now.replace(year=now.year - 1)
        except ValueError:
            # Feb 29 in a leap year — fall back to Feb 28
            one_year_ago = now.replace(year=now.year - 1, day=28)
        return one_year_ago.timestamp(), now.timestamp()
    else:
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        return start.timestamp(), end.timestamp()


def filter_by_year(post: dict, year: int) -> bool:
    """Filter posts created within the target year's date range."""
    created = post.get("created_utc", 0)
    start, end = date_range_for_year(year)
    return start <= created <= end


def score_post(post: dict) -> int:
    """Simple engagement score combining upvotes and comment count."""
    return post.get("score", 0) + post.get("num_comments", 0) * 3


def main():
    parser = argparse.ArgumentParser(description="Fetch game subreddit posts for idea research")
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year for filtering posts (default: current year)")
    parser.add_argument("--limit", type=int, default=25,
                        help="Max posts to fetch per subreddit (default: 25)")
    parser.add_argument("--output", type=str, default="/tmp/reddit_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--subreddits", type=str, default=None,
                        help="Comma-separated subreddit list (default: built-in game list)")
    args = parser.parse_args()

    subreddits = args.subreddits.split(",") if args.subreddits else GAME_SUBREDDITS
    target_year = args.year

    print(f"Fetching posts from {len(subreddits)} subreddits for year {target_year}...")

    all_posts = []
    pain_posts = []
    posts_by_subreddit: dict[str, list[dict]] = {}

    for sub in subreddits:
        print(f"  Fetching r/{sub}...")
        posts = fetch_subreddit_posts(sub, limit=args.limit, sort="top", target_year=target_year)

        sub_entries = []
        for post in posts:
            # Apply strict year filter client-side
            if not filter_by_year(post, target_year):
                continue

            entry = {
                "subreddit": sub,
                "title": post.get("title", ""),
                "selftext": post.get("selftext", "")[:500],  # truncate for storage
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "flair": post.get("link_flair_text", ""),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "created_utc": post.get("created_utc", 0),
                "engagement_score": score_post(post),
                "is_pain_point": is_pain_point(post),
            }
            all_posts.append(entry)
            sub_entries.append(entry)
            if entry["is_pain_point"]:
                pain_posts.append(entry)

        if sub_entries:
            sub_entries.sort(key=lambda x: x["engagement_score"], reverse=True)
            posts_by_subreddit[sub] = sub_entries

        time.sleep(1)  # be polite to Reddit's API

    # Sort by engagement
    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    pain_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(all_posts),
        "pain_point_posts": len(pain_posts),
        "subreddits_searched": subreddits,
        "top_pain_points": pain_posts[:50],
        # Top 100 cross-subreddit posts by engagement (dominated by large subreddits).
        # Use posts_by_subreddit for niche-specific analysis.
        "all_posts": all_posts[:100],
        # All fetched posts grouped by subreddit — use this when filtering by genre/market
        # (e.g. posts_by_subreddit["cozygames"] for cozy game research).
        "posts_by_subreddit": posts_by_subreddit,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Fetched {len(all_posts)} posts, {len(pain_posts)} flagged as pain points.")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()

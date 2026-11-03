"""Round-trip a value through the Redis cache (needs Redis running).

Run from the repo root:  python -m scripts.check_cache
"""
from datetime import datetime

from app.utils.cache import cache_events, get_cached_events

if __name__ == "__main__":
    cache_events("events:check", [{"id": 1, "timestamp": datetime.now()}], expiration=60)
    print("Cached data:", get_cached_events("events:check"))

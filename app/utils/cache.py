"""Optional Redis cache for event log listings.

If Redis is unreachable (or CACHE_ENABLED=false) every function degrades to a no-op,
so the API keeps working straight from the database.
"""
import json
import logging
from datetime import datetime

import redis

from app.config import settings

logger = logging.getLogger(__name__)

EVENTS_PREFIX = "events:"

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def cache_events(key: str, events: list, expiration: int = settings.CACHE_EXPIRATION):
    """Cache a list of event dicts in Redis."""
    if not settings.CACHE_ENABLED:
        return
    try:
        redis_client.setex(key, expiration, json.dumps(events, cls=DateTimeEncoder))
    except redis.RedisError as e:
        logger.warning(f"Redis unavailable, not caching '{key}': {e}")


def get_cached_events(key: str):
    """Return cached events for `key`, or None on a miss / when Redis is unavailable."""
    if not settings.CACHE_ENABLED:
        return None
    try:
        cached_data = redis_client.get(key)
    except redis.RedisError as e:
        logger.warning(f"Redis unavailable, skipping cache for '{key}': {e}")
        return None
    return json.loads(cached_data) if cached_data is not None else None


def invalidate_events_cache():
    """Drop every cached event listing (call after any write to event_logs)."""
    if not settings.CACHE_ENABLED:
        return
    try:
        keys = list(redis_client.scan_iter(f"{EVENTS_PREFIX}*"))
        if keys:
            redis_client.delete(*keys)
    except redis.RedisError as e:
        logger.warning(f"Redis unavailable, could not invalidate cache: {e}")

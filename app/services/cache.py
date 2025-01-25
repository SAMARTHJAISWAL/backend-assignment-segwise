import json
import logging
from redis import StrictRedis

logger = logging.getLogger(__name__)
redis_client = StrictRedis(host="localhost", port=6379, decode_responses=True)

def serialize_event(event):
    if isinstance(event, dict):
        for key, value in event.items():
            if isinstance(value, datetime):
                event[key] = value.isoformat()
    return event

def cache_events(key: str, events: list, expiration: int = 3600):
    try:
        redis_client.setex(key, expiration, json.dumps(events, default=str))
        logger.info(f"Cached {len(events)} events with key '{key}'.")
    except Exception as e:
        logger.error(f"Error caching events with key '{key}': {e}")


def get_cached_events(key):
    cached = cache.get(key)
    return json.loads(cached) if cached else None

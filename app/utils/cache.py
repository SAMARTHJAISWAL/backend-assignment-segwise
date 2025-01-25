import redis
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def cache_events(key: str, events: list, expiration: int = 3600):
    """
    Cache event logs in Redis.
    """
    try:
        redis_client.setex(key, expiration, json.dumps(events, cls=DateTimeEncoder))
        logger.info(f"Cached {len(events)} events with key '{key}'.")
    except Exception as e:
        logger.error(f"Error caching events with key '{key}': {e}")

def get_cached_events(key: str):
    """
    Retrieve cached events from Redis.
    """
    try:
        cached_data = redis_client.get(key)
        if cached_data:
            logger.info(f"Retrieved cached events with key '{key}'.")
            return json.loads(cached_data)
        logger.info(f"No cached data found for key '{key}'.")
        return None
    except Exception as e:
        logger.error(f"Error retrieving cached events with key '{key}': {e}")
        return None

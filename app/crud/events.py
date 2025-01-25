from sqlalchemy.orm import Session
from app.models import EventLog
from app.utils.cache import cache_events, get_cached_events
import logging

logger = logging.getLogger(__name__)

def log_event(db: Session, trigger_id: int, details: str, archived: bool = False):
    """
    Log an event in the database.
    """
    try:
        event = EventLog(trigger_id=trigger_id, details=details, archived=archived)
        db.add(event)
        db.commit()
        db.refresh(event)
        logger.info(f"Event logged: {event}")
        return event
    except Exception as e:
        logger.error(f"Error logging event: {e}")
        raise

def get_events(db: Session, archived: bool = False, use_cache: bool = True):
    """
    Retrieve events from the database, optionally using Redis cache.

    :param db: Database session.
    :param archived: Whether to retrieve archived events.
    :param use_cache: Whether to use cached events from Redis.
    :return: List of events.
    """
    cache_key = f"events:archived:{archived}"

    if use_cache:
        # Attempt to retrieve from cache
        cached_events = get_cached_events(cache_key)
        if cached_events:
            logger.info(f"Using cached events for key '{cache_key}'.")
            return cached_events

    # Fetch from the database
    try:
        events = db.query(EventLog).filter(EventLog.archived == archived).all()
        event_data = [
            {
                "id": e.id,
                "trigger_id": e.trigger_id,
                "details": e.details,
                "timestamp": e.timestamp.isoformat(),
                "archived": e.archived,
            }
            for e in events
        ]

        # Cache the result
        cache_events(cache_key, event_data)
        logger.info(f"Fetched and cached {len(event_data)} events for key '{cache_key}'.")
        return event_data
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        raise

def archive_event(db: Session, event_id: int):
    """
    Archive an event in the database.
    """
    try:
        event = db.query(EventLog).filter(EventLog.id == event_id).first()
        if not event:
            logger.warning(f"Event with ID {event_id} not found.")
            return None
        event.archived = True
        db.commit()

        # Clear related cache
        cache_key = "events:archived:false"
        cache_events(cache_key, [])  # Clear non-archived events from cache
        logger.info(f"Archived event {event_id} and cleared related cache.")
        return event
    except Exception as e:
        logger.error(f"Error archiving event {event_id}: {e}")
        raise

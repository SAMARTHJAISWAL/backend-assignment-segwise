import logging

from sqlalchemy.orm import Session

from app.models import EventLog
from app.utils.cache import invalidate_events_cache

logger = logging.getLogger(__name__)


def log_event(db: Session, trigger_id: int, details: str, archived: bool = False) -> EventLog:
    """Insert an event log row and invalidate cached event listings."""
    event = EventLog(trigger_id=trigger_id, details=details, archived=archived)
    db.add(event)
    db.commit()
    db.refresh(event)
    invalidate_events_cache()
    logger.info(f"Event logged: {event}")
    return event

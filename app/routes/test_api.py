from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.utils.cache import cache_events
from app.crud.events import log_event, get_events
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/")
def test_trigger(payload: dict, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received payload: {payload}")
        
        # Log the event
        event = log_event(db, trigger_id=0, details=f"Test trigger executed with payload: {payload}")
        logger.info(f"Event logged successfully: {event}")
        
        # Update the cache
        cache_key = "events:archived:False"
        active_events = get_events(db, archived=False, use_cache=False)  # Fetch updated data
        cache_events(cache_key, active_events)  # Update cache
        logger.info(f"Cache updated for key '{cache_key}' with {len(active_events)} events.")

        return {"message": "Test trigger fired", "payload": payload}
    except Exception as e:
        logger.error(f"Error logging event: {e}")
        return {"message": "Failed to log event", "error": str(e)}

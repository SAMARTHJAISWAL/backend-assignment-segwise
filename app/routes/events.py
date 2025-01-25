from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils.db import get_db
from app.models import EventLog
from app.schemas import EventLogSchema
from app.utils.cache import get_cached_events, cache_events
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/aggregate")
def aggregate_events(db: Session = Depends(get_db)):
    try:
        results = (
            db.query(EventLog.trigger_id, func.count(EventLog.id).label("count"))
            .group_by(EventLog.trigger_id)
            .all()
        )
        return [{"trigger_id": r[0], "count": r[1]} for r in results]
    except Exception as e:
        logger.error(f"Error aggregating events: {e}")
        raise HTTPException(status_code=500, detail="Failed to aggregate events")

@router.get("/")
def list_event_logs(
    archived: bool = False,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    cache_key = f"events:archived:{archived}:page:{page}:limit:{limit}"
    cached_events = get_cached_events(cache_key)

    if cached_events:
        logger.info(f"Using cached events for key: {cache_key}")
        return cached_events

    offset = (page - 1) * limit
    try:
        events = (
            db.query(EventLog)
            .filter(EventLog.archived == archived)
            .order_by(EventLog.timestamp.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        event_list = [EventLogSchema.from_orm(e).dict() for e in events]

        cache_events(cache_key, event_list, expiration=3600)
        return event_list
    except Exception as e:
        logger.error(f"Error fetching event logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch events")

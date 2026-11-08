import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import EventLog
from app.schemas import EventLogSchema
from app.utils.cache import EVENTS_PREFIX, cache_events, get_cached_events
from app.utils.db import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/aggregate")
def aggregate_events(db: Session = Depends(get_db)):
    """Number of logged events per trigger."""
    results = (
        db.query(EventLog.trigger_id, func.count(EventLog.id).label("count"))
        .group_by(EventLog.trigger_id)
        .all()
    )
    return [{"trigger_id": trigger_id, "count": count} for trigger_id, count in results]


@router.get("/", response_model=list[EventLogSchema])
def list_event_logs(
    archived: bool = False,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Paginated event logs, newest first. Cached in Redis when available."""
    cache_key = f"{EVENTS_PREFIX}archived:{archived}:page:{page}:limit:{limit}"
    cached = get_cached_events(cache_key)
    if cached is not None:
        return cached

    events = (
        db.query(EventLog)
        .filter(EventLog.archived.is_(archived))
        .order_by(EventLog.timestamp.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    event_list = [EventLogSchema.model_validate(e).model_dump(mode="json") for e in events]
    cache_events(cache_key, event_list)
    return event_list

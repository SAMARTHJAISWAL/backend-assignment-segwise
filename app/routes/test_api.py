import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.events import log_event
from app.utils.db import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/")
def test_trigger(payload: dict, db: Session = Depends(get_db)):
    """Fire an ad-hoc test trigger: logs an event (trigger_id 0) without saving a trigger."""
    event = log_event(db, trigger_id=0, details=f"Test trigger executed with payload: {payload}")
    return {"message": "Test trigger fired", "payload": payload, "event_id": event.id}

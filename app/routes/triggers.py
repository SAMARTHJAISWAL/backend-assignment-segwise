import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.triggers import create_trigger, delete_trigger, get_triggers
from app.schemas import TriggerCreate, TriggerResponse
from app.services.scheduler import schedule_trigger, unschedule_trigger
from app.utils.auth import validate_api_key
from app.utils.db import get_db

router = APIRouter(dependencies=[Depends(validate_api_key)])
logger = logging.getLogger(__name__)


@router.post("/", response_model=TriggerResponse)
def create_new_trigger(trigger: TriggerCreate, db: Session = Depends(get_db)):
    """Create a trigger. Scheduled triggers are registered with the scheduler."""
    if trigger.type not in ("api", "scheduled"):
        raise HTTPException(status_code=422, detail="Invalid trigger type. Must be 'api' or 'scheduled'.")
    if trigger.type == "scheduled" and not trigger.schedule_time:
        raise HTTPException(status_code=422, detail="Scheduled triggers must include schedule_time")

    new_trigger = create_trigger(db, trigger)
    if new_trigger.type == "scheduled":
        schedule_trigger(new_trigger.id, new_trigger.schedule_time)
    return new_trigger


@router.get("/", response_model=list[TriggerResponse])
def list_triggers(db: Session = Depends(get_db)):
    """List all triggers."""
    return get_triggers(db)


@router.delete("/{trigger_id}")
def remove_trigger(trigger_id: int, db: Session = Depends(get_db)):
    """Delete a trigger (and its event logs) by ID."""
    if delete_trigger(db, trigger_id) is None:
        raise HTTPException(status_code=404, detail="Trigger not found")
    unschedule_trigger(trigger_id)
    return {"message": "Trigger deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import TriggerCreate, TriggerResponse
from app.utils.db import get_db
from app.models import Trigger 
from app.utils.auth import validate_api_key
import logging

# Initialize router
router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/", response_model=TriggerResponse, dependencies=[Depends(validate_api_key)])
def create_new_trigger(trigger: TriggerCreate, db: Session = Depends(get_db)):
    """
    Create a new trigger.
    """
    from app.crud.triggers import create_trigger  # Import moved here to avoid circular dependency

    if trigger.type == "scheduled" and not trigger.schedule_time:
        raise HTTPException(
            status_code=422, detail="Scheduled triggers must include schedule_time"
        )
    if trigger.type not in ["api", "scheduled"]:
        raise HTTPException(
            status_code=422, detail="Invalid trigger type. Must be 'api' or 'scheduled'."
        )

    try:
        new_trigger = create_trigger(db, trigger)
        return new_trigger
    except Exception as e:
        logger.error(f"Error creating trigger: {e}")
        raise HTTPException(status_code=500, detail="Failed to create trigger")

@router.get("/", response_model=list[TriggerResponse], dependencies=[Depends(validate_api_key)])
def list_triggers(db: Session = Depends(get_db)):
    """
    List all triggers.
    """
    triggers = db.query(Trigger).all()
    return [TriggerResponse.from_orm(trigger) for trigger in triggers]

@router.delete("/{trigger_id}", dependencies=[Depends(validate_api_key)])
def remove_trigger(trigger_id: int, db: Session = Depends(get_db)):
    """
    Delete a trigger by ID.
    """
    from app.crud.triggers import delete_trigger  # Import moved here to avoid circular dependency

    try:
        delete_trigger(db, trigger_id)
        return {"message": "Trigger deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting trigger {trigger_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete trigger")

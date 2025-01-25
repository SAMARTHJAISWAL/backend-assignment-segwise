from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import TriggerCreate, TriggerResponse
from app.crud.triggers import create_trigger, get_triggers, delete_trigger
from app.utils.db import get_db
from app.utils.auth import validate_api_key

router = APIRouter()

@router.post("/", response_model=TriggerResponse, dependencies=[Depends(validate_api_key)])
def create_new_trigger(trigger: TriggerCreate, db: Session = Depends(get_db)):
    """
    Create a new trigger.
    """
    return create_trigger(db, trigger)

@router.get("/", response_model=list[TriggerResponse], dependencies=[Depends(validate_api_key)])
def list_triggers(db: Session = Depends(get_db)):
    """
    List all triggers.
    """
    return get_triggers(db)

@router.delete("/{trigger_id}", dependencies=[Depends(validate_api_key)])
def remove_trigger(trigger_id: int, db: Session = Depends(get_db)):
    """
    Delete a trigger by ID.
    """
    delete_trigger(db, trigger_id)
    return {"message": "Trigger deleted successfully"}

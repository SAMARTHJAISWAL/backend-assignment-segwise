from sqlalchemy.orm import Session
from app.models import Trigger
from app.schemas import TriggerCreate

def create_trigger(db: Session, trigger_data: TriggerCreate):
    """
    Create a new trigger in the database.
    """
    new_trigger = Trigger(
        name=trigger_data.name,
        type=trigger_data.type,
        payload=trigger_data.payload,
        schedule_time=trigger_data.schedule_time,
    )
    try:
        db.add(new_trigger)
        db.commit()
        db.refresh(new_trigger)
        return new_trigger
    except Exception as e:
        raise ValueError(f"Database error while creating trigger: {e}")

def get_triggers(db: Session):
    """
    Retrieve all triggers from the database.
    """
    return db.query(Trigger).all()

def delete_trigger(db: Session, trigger_id: int):
    """
    Delete a trigger by ID from the database.
    """
    trigger = db.query(Trigger).filter(Trigger.id == trigger_id).first()
    if not trigger:
        raise ValueError("Trigger not found")
    db.delete(trigger)
    db.commit()

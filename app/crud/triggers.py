from typing import Optional

from sqlalchemy.orm import Session

from app.models import Trigger
from app.schemas import TriggerCreate


def create_trigger(db: Session, trigger_data: TriggerCreate) -> Trigger:
    new_trigger = Trigger(
        name=trigger_data.name,
        type=trigger_data.type,
        payload=trigger_data.payload,
        schedule_time=trigger_data.schedule_time,
    )
    db.add(new_trigger)
    db.commit()
    db.refresh(new_trigger)
    return new_trigger


def get_triggers(db: Session) -> list[Trigger]:
    return db.query(Trigger).all()


def delete_trigger(db: Session, trigger_id: int) -> Optional[Trigger]:
    """Delete a trigger; returns None if it does not exist."""
    trigger = db.get(Trigger, trigger_id)
    if trigger is None:
        return None
    db.delete(trigger)
    db.commit()
    return trigger

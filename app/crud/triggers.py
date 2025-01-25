from sqlalchemy.orm import Session
from app.models import Trigger
from app.schemas import TriggerCreate

def create_trigger(db: Session, trigger: TriggerCreate):
    db_trigger = Trigger(**trigger.dict())
    db.add(db_trigger)
    db.commit()
    db.refresh(db_trigger)
    return db_trigger

def get_triggers(db: Session):
    return db.query(Trigger).all()

def delete_trigger(db: Session, trigger_id: int):
    db.query(Trigger).filter(Trigger.id == trigger_id).delete()
    db.commit()

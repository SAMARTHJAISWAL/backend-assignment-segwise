from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TriggerCreate(BaseModel):
    name: str
    type: str  # "scheduled" or "api"
    payload: Optional[str] = None
    schedule_time: Optional[datetime] = None

class TriggerResponse(BaseModel):
    id: int
    name: str
    type: str
    payload: Optional[str] = None
    schedule_time: Optional[str] = None  # Change to str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            type=obj.type,
            payload=obj.payload,
            schedule_time=obj.schedule_time.isoformat() if obj.schedule_time else None,
            is_active=obj.is_active,
        )

class EventLogSchema(BaseModel):
    id: int
    trigger_id: int
    details: str
    timestamp: datetime
    archived: bool

    class Config:
        from_attributes = True

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
    payload: str
    schedule_time: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class EventLogSchema(BaseModel):
    id: int
    trigger_id: int
    details: str
    timestamp: datetime
    archived: bool

    class Config:
        from_attributes = True

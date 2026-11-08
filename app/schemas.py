from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TriggerCreate(BaseModel):
    name: str
    type: str  # "scheduled" or "api" (validated in the route for a clear error message)
    payload: Optional[str] = None
    schedule_time: Optional[datetime] = None


class TriggerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    payload: Optional[str] = None
    schedule_time: Optional[datetime] = None
    is_active: bool


class EventLogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trigger_id: int
    details: str
    timestamp: datetime
    archived: bool


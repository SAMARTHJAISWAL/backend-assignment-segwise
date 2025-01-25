from sqlalchemy import Column, Integer, String, Boolean, DateTime
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from datetime import datetime

Base = declarative_base()

class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String) 
    payload = Column(String, nullable=True)
    schedule_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    trigger_id = Column(Integer)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    archived = Column(Boolean, default=False)

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)  # Ensure name is required
    type = Column(String, nullable=False)  # Ensure type is required ("scheduled" or "api")
    payload = Column(String, nullable=True)
    schedule_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationship to EventLog
    events = relationship("EventLog", back_populates="trigger", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trigger(id={self.id}, name={self.name}, type={self.type}, is_active={self.is_active})>"

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    trigger_id = Column(Integer, ForeignKey("triggers.id", ondelete="CASCADE"), nullable=False)  # ForeignKey with CASCADE delete
    details = Column(String, nullable=False)  # Ensure details are required
    timestamp = Column(DateTime, default=datetime.utcnow)
    archived = Column(Boolean, default=False)

    # Relationship to Trigger
    trigger = relationship("Trigger", back_populates="events")

    def __repr__(self):
        return f"<EventLog(id={self.id}, trigger_id={self.trigger_id}, archived={self.archived})>"

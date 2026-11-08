from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from app.utils.time import utcnow

Base = declarative_base()


class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)  # "scheduled" or "api"
    payload = Column(String, nullable=True)
    schedule_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    events = relationship("EventLog", back_populates="trigger", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trigger(id={self.id}, name={self.name}, type={self.type}, is_active={self.is_active})>"


class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    # trigger_id 0 is used for ad-hoc test events that are not tied to a saved trigger.
    trigger_id = Column(Integer, ForeignKey("triggers.id", ondelete="CASCADE"), nullable=False)
    details = Column(String, nullable=False)
    timestamp = Column(DateTime, default=utcnow)
    archived = Column(Boolean, default=False)

    trigger = relationship("Trigger", back_populates="events")

    def __repr__(self):
        return f"<EventLog(id={self.id}, trigger_id={self.trigger_id}, archived={self.archived})>"

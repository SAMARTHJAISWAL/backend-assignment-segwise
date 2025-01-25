from app.utils.db import SessionLocal
from app.models import EventLog

db = SessionLocal()
events = db.query(EventLog).all()
for event in events:
    print(event.id, event.trigger_id, event.details, event.archived, event.timestamp)
db.close()

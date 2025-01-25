from app.models import EventLog
from app.utils.db import SessionLocal

db = SessionLocal()

# Add a sample event
event = EventLog(
    trigger_id=1,
    details="Manually added event for testing",
    archived=False
)

db.add(event)
db.commit()
db.close()

print("Sample event added successfully!")

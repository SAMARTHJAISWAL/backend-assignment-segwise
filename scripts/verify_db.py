"""Print every event log in the database.

Run from the repo root:  python -m scripts.verify_db
"""
from app.models import EventLog
from app.utils.db import SessionLocal

if __name__ == "__main__":
    with SessionLocal() as db:
        for log in db.query(EventLog).order_by(EventLog.id).all():
            print(
                f"ID: {log.id}, Trigger ID: {log.trigger_id}, Details: {log.details}, "
                f"Timestamp: {log.timestamp}, Archived: {log.archived}"
            )

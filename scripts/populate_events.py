"""Insert sample event logs, including some older than 48 hours to exercise cleanup.

Run from the repo root:  python -m scripts.populate_events
"""
from datetime import timedelta

from app.models import EventLog
from app.utils.db import SessionLocal, init_db
from app.utils.time import utcnow


def add_sample_event():
    with SessionLocal() as db:
        db.add(EventLog(trigger_id=0, details="Sample event for testing", archived=False))
        db.commit()
    print("Sample event added.")


def populate_old_logs():
    old = utcnow() - timedelta(days=3)
    with SessionLocal() as db:
        for i in range(5):
            db.add(EventLog(trigger_id=0, details=f"Old log {i}", timestamp=old, archived=True))
        db.commit()
    print("Old logs added for cleanup testing.")


if __name__ == "__main__":
    init_db()
    add_sample_event()
    populate_old_logs()

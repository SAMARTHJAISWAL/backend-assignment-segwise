from datetime import datetime, timedelta
from app.models import EventLog
from app.utils.db import SessionLocal


def add_sample_event():
    """
    Add a single sample event log for testing.
    """
    with SessionLocal() as db:
        try:
            # Add a sample event log
            event = EventLog(
                trigger_id=1,  # Reference to an existing trigger ID
                details="Sample event for testing",
                archived=False,
                timestamp=datetime.now(),
            )
            db.add(event)
            db.commit()
            print("Sample event added successfully!")
        except Exception as e:
            print(f"Error adding sample event: {e}")


def populate_old_logs():
    """
    Add sample logs older than 48 hours for testing cleanup.
    """
    with SessionLocal() as db:
        try:
            cutoff_time = datetime.now() - timedelta(days=3)
            for i in range(5):
                log = EventLog(
                    trigger_id=1,
                    details=f"Old log {i}",
                    timestamp=cutoff_time,
                    archived=True,
                )
                db.add(log)
            db.commit()
            print("Old logs added for testing.")
        except Exception as e:
            print(f"Error populating old logs: {e}")


if __name__ == "__main__":
    # Add a single sample event log
    add_sample_event()

    # Populate old logs for cleanup testing
    populate_old_logs()

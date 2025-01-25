import os
import sys
from datetime import datetime
from app.utils.db import SessionLocal
from app.models import EventLog

# Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def verify_database():
    """
    Print all logs in the database for verification.
    """
    with SessionLocal() as db:
        all_logs = db.query(EventLog).all()
        print("Current logs in database:")
        for log in all_logs:
            print(f"ID: {log.id}, Trigger ID: {log.trigger_id}, Details: {log.details}, "
                  f"Timestamp: {log.timestamp}, Archived: {log.archived}")

if __name__ == "__main__":
    verify_database()

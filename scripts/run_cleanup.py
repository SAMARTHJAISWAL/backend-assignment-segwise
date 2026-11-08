"""Run the event-retention jobs once (archive after 2h, delete after 48h).

Run from the repo root:  python -m scripts.run_cleanup
"""
from app.services.scheduler import archive_old_events, cleanup_old_logs

if __name__ == "__main__":
    print(f"Archived {archive_old_events()} events.")
    print(f"Deleted {cleanup_old_logs()} events.")

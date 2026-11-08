"""Schedule three log-only jobs 10/20/30 seconds out and watch them fire.

Run from the repo root:  python -m scripts.demo_scheduler
(Jobs log events for trigger IDs 1-3; they are skipped if those triggers don't exist.)
"""
import time
from datetime import datetime, timedelta

from app.services.scheduler import schedule_trigger, scheduler
from app.utils.db import init_db

if __name__ == "__main__":
    init_db()
    scheduler.start()
    for i, delay in enumerate((10, 20, 30), start=1):
        schedule_trigger(trigger_id=i, schedule_time=datetime.now() + timedelta(seconds=delay))
    print("Waiting for the jobs to execute (Ctrl+C to stop)...")
    try:
        time.sleep(35)
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.shutdown()

from datetime import datetime, timedelta
from app.crud.events import log_event
from app.utils.db import SessionLocal
from app.models import EventLog
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def execute_trigger(trigger_id):
    try:
        with SessionLocal() as db:
            log_event(db, trigger_id=trigger_id, details="Scheduled trigger executed.")
        logger.info(f"Trigger {trigger_id} executed successfully at {datetime.now()}")
    except Exception as e:
        logger.error(f"Error executing trigger {trigger_id}: {e}")

def schedule_trigger(trigger_id, schedule_time):
    try:
        scheduler.add_job(
            func=execute_trigger,
            trigger="date",
            run_date=schedule_time,
            args=[trigger_id],
            id=str(trigger_id), 
            replace_existing=True  
        )
        logger.info(f"Trigger {trigger_id} scheduled for {schedule_time}")
    except Exception as e:
        logger.error(f"Error scheduling trigger {trigger_id}: {e}")

def cleanup_archived_events():
    try:
        with SessionLocal() as db:
            cutoff_time = datetime.now() - timedelta(hours=48)
            deleted = db.query(EventLog).filter(
                EventLog.archived == True, EventLog.timestamp < cutoff_time
            ).delete()
            db.commit()
            logger.info(f"Deleted {deleted} archived events older than 48 hours.")
    except Exception as e:
        logger.error(f"Error during cleanup of archived events: {e}")

def cleanup_old_logs():
    try:
        with SessionLocal() as db:
            cutoff_time = datetime.now() - timedelta(hours=48)
            deleted_rows = (
                db.query(EventLog).filter(EventLog.timestamp < cutoff_time).delete()
            )
            db.commit()
            logger.info(f"Deleted {deleted_rows} logs older than 48 hours.")
    except Exception as e:
        logger.error(f"Error during cleanup of old logs: {e}")

def start_scheduler():
    try:
        scheduler.start()
        logger.info("Scheduler started successfully.")
    except Exception as e:
        logger.error(f"Error starting the scheduler: {e}")

def shutdown_scheduler():
    try:
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully.")
    except Exception as e:
        logger.error(f"Error shutting down the scheduler: {e}")

scheduler.add_job(
    func=cleanup_archived_events,
    trigger="interval",
    hours=1,
    id="cleanup_archived_events",
    replace_existing=True,
)

scheduler.add_job(
    func=cleanup_old_logs,
    trigger="interval",
    hours=1,
    id="cleanup_old_logs",
    replace_existing=True,
)

import logging
from datetime import datetime, timedelta

from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings
from app.crud.events import log_event
from app.models import EventLog, Trigger
from app.utils.cache import invalidate_events_cache
from app.utils.db import SessionLocal
from app.utils.time import utcnow

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def _job_id(trigger_id: int) -> str:
    return f"trigger-{trigger_id}"


def execute_trigger(trigger_id: int):
    """Fire a scheduled trigger: log an event and mark the (one-time) trigger inactive."""
    try:
        with SessionLocal() as db:
            trigger = db.get(Trigger, trigger_id)
            if trigger is None:
                logger.warning(f"Trigger {trigger_id} no longer exists; skipping.")
                return
            details = "Scheduled trigger executed."
            if trigger.payload:
                details += f" Payload: {trigger.payload}"
            log_event(db, trigger_id=trigger_id, details=details)
            trigger.is_active = False
            db.commit()
        logger.info(f"Trigger {trigger_id} executed at {datetime.now()}")
    except Exception as e:
        logger.error(f"Error executing trigger {trigger_id}: {e}")


def schedule_trigger(trigger_id: int, schedule_time: datetime):
    """Schedule a one-time job. Past times run immediately (APScheduler misfire grace)."""
    scheduler.add_job(
        func=execute_trigger,
        trigger="date",
        run_date=schedule_time,
        args=[trigger_id],
        id=_job_id(trigger_id),
        replace_existing=True,
        misfire_grace_time=None,
    )
    logger.info(f"Trigger {trigger_id} scheduled for {schedule_time}")


def unschedule_trigger(trigger_id: int):
    try:
        scheduler.remove_job(_job_id(trigger_id))
    except JobLookupError:
        pass


def reschedule_pending_triggers():
    """Jobs live in memory, so re-register active scheduled triggers after a restart."""
    with SessionLocal() as db:
        pending = (
            db.query(Trigger)
            .filter(Trigger.type == "scheduled", Trigger.is_active.is_(True))
            .filter(Trigger.schedule_time.isnot(None))
            .all()
        )
        for trigger in pending:
            schedule_trigger(trigger.id, trigger.schedule_time)
    return len(pending)


def archive_old_events():
    """Move events older than ACTIVE_RETENTION_HOURS from active to archived."""
    cutoff = utcnow() - timedelta(hours=settings.ACTIVE_RETENTION_HOURS)
    with SessionLocal() as db:
        archived = (
            db.query(EventLog)
            .filter(EventLog.archived.is_(False), EventLog.timestamp < cutoff)
            .update({EventLog.archived: True}, synchronize_session=False)
        )
        db.commit()
    if archived:
        invalidate_events_cache()
    logger.info(f"Archived {archived} events older than {settings.ACTIVE_RETENTION_HOURS} hours.")
    return archived


def cleanup_old_logs():
    """Delete events older than TOTAL_RETENTION_HOURS (active or archived)."""
    cutoff = utcnow() - timedelta(hours=settings.TOTAL_RETENTION_HOURS)
    with SessionLocal() as db:
        deleted = (
            db.query(EventLog)
            .filter(EventLog.timestamp < cutoff)
            .delete(synchronize_session=False)
        )
        db.commit()
    if deleted:
        invalidate_events_cache()
    logger.info(f"Deleted {deleted} logs older than {settings.TOTAL_RETENTION_HOURS} hours.")
    return deleted


def run_retention_jobs():
    try:
        archive_old_events()
        cleanup_old_logs()
    except Exception as e:
        logger.error(f"Error running retention jobs: {e}")


scheduler.add_job(
    func=run_retention_jobs,
    trigger="interval",
    minutes=10,
    id="retention",
    replace_existing=True,
)

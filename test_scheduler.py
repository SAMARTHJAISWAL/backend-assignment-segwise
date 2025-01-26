from datetime import datetime, timedelta
from app.services.scheduler import schedule_trigger, scheduler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_scheduling():
    logger.info("Starting test scheduling...")
    schedule_trigger(trigger_id=1, schedule_time=datetime.now() + timedelta(seconds=10))
    logger.info("Trigger 1 scheduled to execute in 10 seconds.")
    
    schedule_trigger(trigger_id=2, schedule_time=datetime.now() + timedelta(seconds=20))
    logger.info("Trigger 2 scheduled to execute in 20 seconds.")
    
    schedule_trigger(trigger_id=3, schedule_time=datetime.now() + timedelta(seconds=30))
    logger.info("Trigger 3 scheduled to execute in 30 seconds.")

if __name__ == "__main__":
    test_scheduling()
    print("Test scheduler is running. Waiting for the jobs to execute...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down the scheduler...")
        scheduler.shutdown()
        print("Scheduler shut down.")

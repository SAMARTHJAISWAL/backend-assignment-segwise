import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import events, test_api, triggers
from app.services.scheduler import reschedule_pending_triggers, scheduler
from app.utils.db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    scheduler.start()
    count = reschedule_pending_triggers()
    logger.info(f"Scheduler started ({count} pending scheduled triggers restored)")
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler shut down")


app = FastAPI(title="Event Trigger Platform", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triggers.router, prefix="/triggers", tags=["Triggers"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(test_api.router, prefix="/test", tags=["Test API"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Trigger Platform!"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import triggers, events, test_api
from app.services.scheduler import scheduler
from app.utils.auth import validate_api_key
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        scheduler.start()
        logger.info("Scheduler started")
        yield
    finally:
        scheduler.shutdown()
        logger.info("Scheduler shut down")

# Create the FastAPI app with lifespan
app = FastAPI(title="Event Trigger Platform", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Explicitly allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(triggers.router, prefix="/triggers", tags=["Triggers"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(test_api.router, prefix="/test", tags=["Test API"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Trigger Platform!"}

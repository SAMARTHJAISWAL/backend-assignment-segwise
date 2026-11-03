import logging
import secrets

from fastapi import Header, HTTPException

from app.config import settings

logger = logging.getLogger(__name__)


def validate_api_key(x_api_key: str = Header(...)):
    """Reject requests whose X-API-KEY header does not match SECRET_API_KEY."""
    if not secrets.compare_digest(x_api_key, settings.SECRET_API_KEY):
        logger.warning("Invalid API key provided.")
        raise HTTPException(status_code=401, detail="Not authenticated")

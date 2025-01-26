import logging
from fastapi import HTTPException, Header

logger = logging.getLogger(__name__)

def validate_api_key(x_api_key: str = Header(...)):
    """
    Validates the provided API key in the request header.
    """
    logger.info(f"Received API Key: {x_api_key}")
    if x_api_key != "your-secure-secret-key-123456":
        logger.warning("Invalid API key provided.")
        raise HTTPException(status_code=401, detail="Not authenticated")

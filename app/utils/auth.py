import os
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key_header = APIKeyHeader(name="X-API-KEY")
SECRET_API_KEY = os.getenv("SECRET_API_KEY")

def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

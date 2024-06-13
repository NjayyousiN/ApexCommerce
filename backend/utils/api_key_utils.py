import secrets
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


# This function generates a random API key
def generateAPIKey():
    return secrets.token_urlsafe(32)


# This function verifies the API key
def verifyAPIKey(key: str):
    return key == API_KEY


# This function verifies a request's API key
def verifyRequestAPIKey(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail="Access token header not found")
    if not verifyAPIKey(api_key):
        raise HTTPException(status_code=403, detail="Invalid API Key")

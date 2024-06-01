from fastapi import Security
from fastapi import security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=1)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired", "status": 401}
    except jwt.PyJWTError:
        return {"error": "Invalid token", "status": 401}

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    return decode_access_token(credentials.credentials)
from pydantic import BaseModel
from typing import Optional

# This model is used to validate the request body for the /auth endpoint
class AuthRequest(BaseModel):
    email: str
    password: str

# This model is used to validate the request body for the /customers endpoint
class CustomerBody(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    phoneNumber: str
    address: str
    password: Optional[str] = None

    class Config:
        from_attributes = True

# This model is used to validate the response body for all endpoints
# `data` can be a string, dictionary, or list
class Response(BaseModel):
    status: int
    data: str | dict | list

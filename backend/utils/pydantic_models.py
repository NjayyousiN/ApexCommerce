from pydantic import BaseModel
from typing import Optional

# This model is used to validate the request body for the /customers endpoint
class UserBody(BaseModel):
    id: Optional[int] = None
    name: str
    phoneNumber: str
    address: str
    email: str
    password: Optional[str] = None

    class Config:
        from_attributes = True

# This model is used to validate the request body for the /items endpoint
class ItemBody(BaseModel):
    itemId: Optional[int] = None
    item_name: str
    rating: Optional[int] = None
    category: str
    itemDesc: str
    stock: int
    itemPic: str
    reviews: Optional[list] = None

    class Config:
        from_attributes = True

# This model is used to validate the request body for the /orders endpoint
class OrderBody(BaseModel):
    orderId: Optional[int] = None
    userId: Optional[int] = None
    items: list[ItemBody]

    class Config:
        from_attributes = True
# This model is used to validate the request body for the /auth endpoint
class AuthRequest(BaseModel):
    email: str
    password: str

# This model is used to validate the response body for all endpoints
# `data` can be a string, dictionary, or list
class Response(BaseModel):
    status: int
    data: str | dict | list 

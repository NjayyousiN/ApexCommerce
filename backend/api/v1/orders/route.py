import json
from db.CRUD import (
    create_order,
    delete_order_by_id,
    read_order_by_id,
    read_orders,
    add_item_to_order,
    read_order_by_userId,
)
from db.session import get_db
from utils.pydantic_models import OrderBody, Response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

# Create a new order
@router.post("/", response_model=Response)
def create_new_order(order: OrderBody, db: Session = Depends(get_db)):
    # Check for any missing required fields
    if not order.items:
        raise HTTPException(status_code=400, detail="Missing data in the request body")
    
    new_order = create_order(
        session=db,
        userId=order.userId,
        # Convert each `ItemBody` object to a `dict` object
        items=[item.model_dump() for item in order.items],
    )
    if new_order:
        return Response(status=200, data=f"order {new_order.orderId} created successfully")
    else:
        raise HTTPException(status_code=400, detail="order not created")

# Read all orders
@router.get("/", response_model=Response)
def get_all_orders(db: Session = Depends(get_db)):
    orders = read_orders(session=db)
    for order in orders:
        order.items = json.loads(order.items)
    orders_data = [OrderBody.model_validate(order) for order in orders]
    return Response(status=200, data={"orders": orders_data})

# Read order by id
@router.get("/{orderId}", response_model=Response)
def get_order_by_id(orderId: int, db: Session = Depends(get_db)):
    order = read_order_by_id(session=db, orderId=orderId)
    if order:
        order.items = json.loads(order.items)
        return Response(status=200, data={"orders": OrderBody.model_validate(order)})
    else:
        raise HTTPException(status_code=404, detail="order not found")

# Read order by userId
@router.get("/user/{userId}", response_model=Response)
def get_order_by_userId(userId: int, db: Session = Depends(get_db)):
    order = read_order_by_userId(session=db, userId=userId)
    if order:
        order.items = json.loads(order.items)
        return Response(status=200, data={"orders": OrderBody.model_validate(order)})
    else:
        raise HTTPException(status_code=404, detail="order not found")
    
# Add an item to an order
@router.post("/{orderId}/items/{itemId}", response_model=Response)
def add_to_order(orderId: int, itemId: int, db: Session = Depends(get_db)):
    order = add_item_to_order(session=db, orderId=orderId, itemId=itemId)
    if order:
        return Response(status=200, data=f"item {itemId} added to order {orderId}")
    else:
        raise HTTPException(status_code=404, detail="order not found")
    
# Delete an order by id
@router.delete("/{orderId}", response_model=Response)
def delete_order(orderId: int, db: Session = Depends(get_db)):
    order = delete_order_by_id(session=db, orderId=orderId)
    if order:
        return Response(status=200, data=f"order {orderId} deleted successfully")
    else:
        raise HTTPException(status_code=404, detail="order not found")
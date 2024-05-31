from db.CRUD import (
    create_item,
    delete_item_by_id,
    read_item_by_id,
    read_items,
    update_item_by_id,
    read_item_by_userId,
    read_item_by_category,
    add_item_to_user,
)
from db.session import get_db
from utils.pydantic_models import ItemBody, Response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

# Create a new item
@router.post("/", response_model=Response)
def create_new_item(item: ItemBody, db: Session = Depends(get_db)):
    # Check for any missing required fields
    if (
        not item.category
        or not item.item_name
        or not item.itemDesc
        or not item.stock
        or not item.itemPic
    ):
        raise HTTPException(status_code=400, detail="Missing data in the request body")

    new_item = create_item(
        db,
        item_name=item.item_name,
        category=item.category,
        itemDesc=item.itemDesc,
        stock=item.stock,
        itemPic=item.itemPic,
    )
    if new_item:
        return Response(status=200, data=f"item {new_item.itemId} created successfully")
    else:
        raise HTTPException(status_code=400, detail="item not created")

# Get all items
@router.get("/", response_model=Response)
def get_all_items(db: Session = Depends(get_db)):
    items = read_items(db)
    items_data = [ItemBody.model_validate(item) for item in items]
    return Response(status=200, data={"items": items_data})

# Get an item by ID
@router.get("/{itemId}", response_model=Response)
def get_item_by_id(itemId: int, db: Session = Depends(get_db)):
    item = read_item_by_id(db, itemId)
    if item:
        return Response(status=200, data={"item": ItemBody.model_validate(item)})
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Get an item by userId
@router.get("/user/{userId}", response_model=Response)
def get_item_by_user(userId: int, db: Session = Depends(get_db)):
    items = read_item_by_userId(db, userId)
    items_data = [ItemBody.model_validate(item) for item in items]
    return Response(status=200, data={"items": items_data})

# Get items by category
@router.get("/category/{category}", response_model=Response)
def get_items_by_category(category: str, db: Session = Depends(get_db)):
    items = read_item_by_category(db, category)
    items_data = [ItemBody.model_validate(item) for item in items]
    return Response(status=200, data={"items": items_data})

# Update an item by ID
@router.put("/{itemId}", response_model=Response)
def update_item(itemId: int, item: ItemBody, db: Session = Depends(get_db)):
    # Check if the item exists
    itemExists = True if read_item_by_id(db, itemId) else False
    if not itemExists:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = update_item_by_id(
        db,
        itemId=itemId,
        item_name=item.item_name,
        category=item.category,
        itemDesc=item.itemDesc,
        stock=item.stock,
        itemPic=item.itemPic,
    )
    if updated_item:
        return Response(status=200, data=f"item {updated_item.itemId} updated successfully")
    else:
        raise HTTPException(status_code=400, detail="item not updated")
    
# Delete an item by ID
@router.delete("/{itemId}", response_model=Response)
def delete_item(itemId: int, db: Session = Depends(get_db)):
    # Check if the item exists
    itemExists = True if read_item_by_id(db, itemId) else False
    if not itemExists:
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_item = delete_item_by_id(db, itemId)
    if deleted_item:
        return Response(status=200, data=f"item {deleted_item.itemId} deleted successfully")
    else:
        raise HTTPException(status_code=400, detail="item not deleted")
    
# Add an item to a user
@router.post("/add-item/{userId}/{itemId}", response_model=Response)
def add_item_to_user_route(userId: int, itemId: int, db: Session = Depends(get_db)):
    itemExists = True if read_item_by_id(db, itemId) else False
    if not itemExists:
        raise HTTPException(status_code=404, detail="Item not found")

    user = add_item_to_user(db, userId, itemId)
    if user:
        return Response(status=200, data=f"item {itemId} added to user {userId} successfully")
    else:
        raise HTTPException(status_code=400, detail="item not added to user or user does not exist")
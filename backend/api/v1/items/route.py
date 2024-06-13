import os
import shutil
from typing import Annotated
from utils.jwt_utils import get_current_user
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
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

router = APIRouter()


# Create a new item
@router.post("/", response_model=Response)
def create_new_item(
    category: Annotated[str, Form(...)],
    item_name: Annotated[str, Form(...)],
    itemDesc: Annotated[str, Form(...)],
    stock: Annotated[int, Form(...)],
    itemPic: Annotated[UploadFile, File(...)],
    db: Session = Depends(get_db),
    user_auth=Depends(get_current_user),
):
    # Check for any missing required fields
    if not category or not item_name or not itemDesc or not stock or not itemPic:
        raise HTTPException(status_code=400, detail="Missing data in the request body")

    # Save the uploaded file
    upload_dir = "uploads/"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = os.path.join(upload_dir, itemPic.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(itemPic.file, buffer)

    new_item = create_item(
        db,
        item_name=item_name,
        category=category,
        itemDesc=itemDesc,
        stock=stock,
        itemPic=file_location,  # file path is saved in database
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


# Get items by userId
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
def update_item(
    itemId: int,
    category: Annotated[str, Form(...)],
    item_name: Annotated[str, Form(...)],
    itemDesc: Annotated[str, Form(...)],
    stock: Annotated[int, Form(...)],
    itemPic: Annotated[UploadFile, File(...)],
    db: Session = Depends(get_db),
    user_auth=Depends(get_current_user),
):
    # Check if the item exists
    itemExists = True if read_item_by_id(db, itemId) else False
    if not itemExists:
        raise HTTPException(status_code=404, detail="Item not found")

    # Save the uploaded file
    upload_dir = "uploads/"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = os.path.join(upload_dir, itemPic.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(itemPic.file, buffer)

    updated_item = update_item_by_id(
        db,
        itemId=itemId,
        item_name=item_name,
        category=category,
        itemDesc=itemDesc,
        stock=stock,
        itemPic=file_location,  # file path is updated in database
    )
    if updated_item:
        return Response(
            status=200, data=f"item {updated_item.itemId} updated successfully"
        )
    else:
        raise HTTPException(status_code=400, detail="item not updated")


# Delete an item by ID
@router.delete("/{itemId}", response_model=Response)
def delete_item(
    itemId: int, db: Session = Depends(get_db), user_auth=Depends(get_current_user)
):
    # Check if the item exists
    itemExists = True if read_item_by_id(db, itemId) else False
    if not itemExists:
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_item = delete_item_by_id(db, itemId)
    if deleted_item:
        return Response(
            status=200, data=f"item {deleted_item.itemId} deleted successfully"
        )
    else:
        raise HTTPException(status_code=400, detail="item not deleted")


# Add an item to a user
@router.post("/add-item/{userId}/{itemId}", response_model=Response)
def add_item_to_user_route(
    userId: int,
    itemId: int,
    db: Session = Depends(get_db),
    user_auth=Depends(get_current_user),
):
    itemExists = True if read_item_by_id(db, itemId) else False
    if not itemExists:
        raise HTTPException(status_code=404, detail="Item not found")

    user = add_item_to_user(db, userId, itemId)
    if user:
        return Response(
            status=200, data=f"item {itemId} added to user {userId} successfully"
        )
    else:
        raise HTTPException(
            status_code=400, detail="item not added to user or user does not exist"
        )

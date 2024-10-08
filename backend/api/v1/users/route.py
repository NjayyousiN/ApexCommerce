from utils.jwt_utils import get_current_user, create_access_token
from utils.api_key_utils import verifyRequestAPIKey
from db.CRUD import (
    create_user,
    read_users,
    read_user_by_id,
    read_user_by_email,
    update_user_by_id,
    delete_user_by_id,
)
from db.session import get_db
from utils.hashing import hash_password
from utils.pydantic_models import UserBody, Response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


# Create a router
router = APIRouter()


# Create a new user
@router.post("/", response_model=Response)
def create_new_user(user: UserBody, db: Session = Depends(get_db)):
    # Check for any missing required fields
    if (
        not user.name
        or not user.email
        or not user.phoneNumber
        or not user.address
        or not user.password
    ):
        raise HTTPException(status_code=400, detail="Missing data in the request body")

    # Check if the user already exists
    userExists = True if read_user_by_email(db, user.email) else False
    if userExists:
        raise HTTPException(
            status_code=400,
            detail="User already exists, please choose a different email address",
        )

    # Hash the password
    hashed_password = hash_password(user.password)
    new_user = create_user(
        db,
        name=user.name,
        email=user.email,
        phoneNumber=user.phoneNumber,
        address=user.address,
        password=hashed_password,
    )
    if new_user:
        token = create_access_token(data={"sub": new_user.id})
        return Response(status=200, data={"message": f"User {new_user.name} created successfully", "token": token})
    else:
        raise HTTPException(status_code=400, detail="user not created")


# Get all users
@router.get("/", response_model=Response)
def get_all_users(db: Session = Depends(get_db), admin_auth = Depends(verifyRequestAPIKey)):
    users = read_users(db)
    users_data = [UserBody.model_validate(user) for user in users]
    return Response(status=200, data={"users": users_data})


# Get a user by ID
@router.get("/{id}", response_model=Response)
def get_user_by_id(id: int, db: Session = Depends(get_db), admin_auth = Depends(verifyRequestAPIKey)):
    user = read_user_by_id(db, id)
    if user:
        return Response(
            status=200,
            data={"user": UserBody.model_validate(user)},
        )
    else:
        raise HTTPException(status_code=404, detail="user not found")


# Update a user by ID
@router.put("/{id}", response_model=Response)
def update_user(id: int, user: UserBody, db: Session = Depends(get_db), user_auth=Depends(get_current_user)):
    updated_user = update_user_by_id(
        db, id, name=user.name, email=user.email, phoneNumber=user.phoneNumber, address=user.address
    )
    if updated_user:
        return Response(status=201, data=f"user {user.name} updated successfully")
    else:
        raise HTTPException(status_code=404, detail="user not found")


# Delete a user by ID
@router.delete("/{id}", response_model=Response)
def delete_user(id: int, db: Session = Depends(get_db), admin_auth = Depends(verifyRequestAPIKey)):
    deleted_user = delete_user_by_id(db, id)
    if deleted_user:
        return Response(
            status=200, data=f"user {deleted_user.name} deleted successfully"
        )
    else:
        raise HTTPException(status_code=404, detail="user not found")
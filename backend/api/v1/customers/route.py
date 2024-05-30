from db.CRUD import (
    create_customer,
    read_customers,
    read_customer_by_id,
    read_customer_by_email,
    update_customer_by_id,
    delete_customer_by_id,
)
from db.session import get_db
from utils.hashing import hash_password
from utils.pydantic_models import CustomerBody, Response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


# Create a router
router = APIRouter()


# Create a new customer
@router.post("/", response_model=Response)
def create_new_customer(customer: CustomerBody, db: Session = Depends(get_db)):
    # Check for any missing required fields
    if (
        not customer.name
        or not customer.email
        or not customer.phoneNumber
        or not customer.address
        or not customer.password
    ):
        raise HTTPException(status_code=400, detail="Missing data in the request body")

    # Check if the customer already exists
    customerExists = True if read_customer_by_email(db, customer.email) else False
    if customerExists:
        raise HTTPException(status_code=400, detail="User already exists, please choose a different email address")
    
    # Hash the password
    hashed_password = hash_password(customer.password)
    new_customer = create_customer(
        db,
        customer.name,
        customer.email,
        customer.phoneNumber,
        customer.address,
        hashed_password,
    )
    if new_customer:
        return Response(
            status=200, data=f"Customer {new_customer.name} created successfully"
        )
    else:
        raise HTTPException(status_code=400, detail="Customer not created")


# Get all customers
@router.get("/", response_model=Response)
def get_all_customers(db: Session = Depends(get_db)):
    customers = read_customers(db)
    if customers:
        customers_data = [
            CustomerBody.model_validate(customer) for customer in customers
        ]
        return Response(status=200, data={"Customers": customers_data})
    else:
        raise HTTPException(status_code=404, detail="No customers found")


# Get a customer by ID
@router.get("/{id}", response_model=Response)
def get_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = read_customer_by_id(db, id)
    if customer:
        return Response(
            status=200,
            data={
                "name": customer.name,
                "email": customer.email,
                "phoneNumber": customer.phoneNumber,
                "address": customer.address,
            },
        )
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# Update a customer by ID
@router.put("/{id}", response_model=Response)
def update_customer(id: int, customer: CustomerBody, db: Session = Depends(get_db)):
    updated_customer = update_customer_by_id(
        db, id, customer.name, customer.email, customer.phoneNumber, customer.address
    )
    if updated_customer:
        return Response(
            status=201, data=f"Customer {customer.name} updated successfully"
        )
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# Delete a customer by ID
@router.delete("/{id}", response_model=Response)
def delete_customer(id: int, db: Session = Depends(get_db)):
    deleted_customer = delete_customer_by_id(db, id)
    if deleted_customer:
        return Response(
            status=200, data=f"Customer {deleted_customer.name} deleted successfully"
        )
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

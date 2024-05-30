from fastapi import APIRouter, Depends, HTTPException
from db.session import get_db
from db.CRUD import read_customer_by_email, read_seller_by_email
from utils.jwt_utils import create_access_token
from utils.hashing import verify_password
from utils.pydantic_models import AuthRequest, Response

router = APIRouter()


@router.post("/", response_model=dict)
def authenticate(auth_data: AuthRequest, db=Depends(get_db)):
    # Check if the user is a customer
    customer = read_customer_by_email(db, auth_data.email)
    if customer:
        # Check if the password is correct
        if verify_password(auth_data.password, customer.password):
            token = create_access_token(data={"sub": customer.id})
            return Response(
                status=200,
                data={
                    "token": token,
                    "type": "customer",
                    "name": customer.name,
                },
            )

        else:
            raise HTTPException(status_code=401, detail="Invalid password")
    else:
        # Check if the user is a seller
        seller = read_seller_by_email(db, auth_data.email)
        if seller:
            # Check if the password is correct
            if verify_password(auth_data.password, seller.password):
                token = create_access_token(data={"sub": seller.id})
                return Response(
                    status=200,
                    data={
                        "token": token,
                        "type": "seller",
                        "name": seller.name,
                    },
                )
            else:
                raise HTTPException(status_code=401, detail="Invalid password")

    raise HTTPException(status_code=404, detail="User not found")

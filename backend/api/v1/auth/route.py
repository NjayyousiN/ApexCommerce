from fastapi import APIRouter, Depends, HTTPException
from db.session import get_db
from db.CRUD import read_user_by_email
from utils.jwt_utils import create_access_token
from utils.hashing import verify_password
from utils.pydantic_models import AuthRequest, Response

router = APIRouter()


@router.post("/", response_model=Response)
def authenticate(auth_data: AuthRequest, db=Depends(get_db)):
    user = read_user_by_email(db, auth_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(auth_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    token = create_access_token(data={"sub": user.id})
    return Response(status=200, data={"token": token})

from fastapi import Request, HTTPException
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from utils.jwt_utils import decode_access_token

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if "Authorization" not in request.headers:
            raise HTTPException(status_code=403, detail="Authorization header missing")
        auth = request.headers["Authorization"]
        token = auth.split(" ")[1]
        
        try:
            decode_access_token(token)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

        response = await call_next(request)
        return response

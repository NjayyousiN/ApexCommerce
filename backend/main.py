from fastapi import FastAPI
from api.v1.auth.route import router as auth_router
from api.v1.users.route import router as users_router
from api.v1.items.route import router as items_router
from api.v1.orders.route import router as orders_router

# Create a FastAPI instance
app = FastAPI()

# Import the routes
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(users_router, prefix="/api/v1/users")
app.include_router(items_router, prefix="/api/v1/items")
app.include_router(orders_router, prefix="/api/v1/orders")

@app.get("/")  
def read_root():
    return {"Hello": "World"}
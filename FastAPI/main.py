
from fastapi import FastAPI

from users.router import router as user_router
from products.router import router as product_router

app = FastAPI(
    title="Apple Store API",
    description="Backend API for Apple Store E-commerce",
    version="1.0.0"
)

# Register User Router
app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
)

# Register Product Router
app.include_router(
    product_router,
    prefix="/products",
    tags=["Products"]
)


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Apple Store API!"
    }

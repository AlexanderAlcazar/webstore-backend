from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.cart import router as cart_router
from app.routers.orders import router as orders_router
from app.routers.products import router as product_router

app = FastAPI(title="Webstore API")

app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(product_router)


@app.get("/health")
def health():
    """Return an application liveness response."""
    return {"status": "ok"}

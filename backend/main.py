from backend.app.api.customers import router as customers_router
from fastapi import FastAPI
from datetime import datetime
from backend.app.api.health import router as health_router
from backend.app.api.orders import router as orders_router
from backend.app.api.order_items import router as order_items_router
from backend.app.api.products import router as products_router
from backend.app.api.sellers import router as sellers_router
from backend.app.api.payments import router as payments_router
from backend.app.api.reviews import router as reviews_router
from backend.app.api.geolocations import router as geolocations_router
from backend.app.api.categories import router as categories_router
from backend.app.api.analytics import router as analytics_router
from backend.app.api.dashboard import router as dashboard_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import Request
from fastapi.responses import JSONResponse




app = FastAPI(
    title="AWS E-Commerce Data Intelligence Platform",
    description="E-Commerce Data Analytics and Intelligence API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174"
],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"]
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled exception on %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):

    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

    return response
@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):

    logger.info(
        "Request started: %s %s",
        request.method,
        request.url.path
    )

    response = await call_next(request)

    logger.info(
        "Request completed: %s %s | Status: %s",
        request.method,
        request.url.path,
        response.status_code
    )

    return response

@app.get("/")
def home():
    return {
        "message": "AWS E-Commerce Data Intelligence Platform API is running",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI Backend"
    }

@app.get("/api/v1")
def api_info():
    return {
        "project": "AWS E-Commerce Data Intelligence Platform",
        "version": "1.0.0",
        "backend": "FastAPI",
        "database": "PostgreSQL",
        "status": "active"
    }
app.include_router(health_router)
app.include_router(customers_router)
app.include_router(orders_router)
app.include_router(order_items_router)
app.include_router(products_router)
app.include_router(sellers_router)
app.include_router(payments_router)
app.include_router(reviews_router)
app.include_router(geolocations_router)
app.include_router(categories_router)
app.include_router(analytics_router)
app.include_router(dashboard_router)
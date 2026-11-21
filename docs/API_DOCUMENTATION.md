
# AWS E-Commerce Data Intelligence Platform
## API Documentation

### 1. Overview
The backend is developed using Python, FastAPI, SQLAlchemy and PostgreSQL.

It provides REST APIs for e-commerce data management, analytics and dashboard reporting.

### 2. Technology Stack
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Pytest

### 3. Database
Database: PostgreSQL

Database name: ecommerce_intelligence

Tables:
- customers
- orders
- order_items
- products
- sellers
- order_payments
- order_reviews
- geolocation
- category_translations

### 4. Running the Backend

Activate the virtual environment and run from the project root:

```powershell
uvicorn backend.main:app --reload
```

Backend URL:
http://127.0.0.1:8000

Swagger API documentation:
http://127.0.0.1:8000/docs

ReDoc:
http://127.0.0.1:8000/redoc

### 5. API Endpoints

#### General
- GET /

- GET /health

- GET /api/v1

- GET /api/v1/health/database

#### Customers
- GET /api/v1/customers/
- GET /api/v1/customers/{customer_id}

#### Orders
- GET /api/v1/orders/
- GET /api/v1/orders/{order_id}

#### Order Items
- GET /api/v1/order-items/
- GET /api/v1/order-items/{order_id}/{order_item_id}

#### Products
- GET /api/v1/products/
- GET /api/v1/products/{product_id}

#### Sellers
- GET /api/v1/sellers/
- GET /api/v1/sellers/{seller_id}

#### Payments
- GET /api/v1/payments/
- GET /api/v1/payments/{order_id}/{payment_sequential}

#### Reviews
- GET /api/v1/reviews/
- GET /api/v1/reviews/{review_id}/{order_id}

#### Geolocation
- GET /api/v1/geolocations/

#### Categories
- GET /api/v1/categories/

#### Analytics
- GET /api/v1/analytics/overview
- GET /api/v1/analytics/order-status
- GET /api/v1/analytics/payments
- GET /api/v1/analytics/reviews
- GET /api/v1/analytics/monthly-sales
- GET /api/v1/analytics/top-products
- GET /api/v1/analytics/top-categories
- GET /api/v1/analytics/customers
- GET /api/v1/analytics/seller-performance

#### Dashboard
- GET /api/v1/dashboard/

### 6. API Features
- REST API architecture
- Database integration with PostgreSQL
- Pagination and query parameter validation
- Pydantic request/response validation
- Analytics and dashboard endpoints
- Centralized exception handling
- Request logging
- CORS configuration
- HTTP security headers

### 7. ETL Integration
The project includes a Python-based ETL pipeline that loads processed Olist datasets into PostgreSQL.

Run the ETL module from the project root:

```powershell
python -m scripts.load_data_to_postgres
```

### 8. Running Tests

Run the API test suite:

```powershell
python -m pytest tests/test_api.py -v
```

Latest test result:
- Total tests: 25
- Passed: 25
- Failed: 0

### 9. Dataset
Primary dataset: Brazilian E-Commerce Public Dataset by Olist.

Total processed records: 1,550,922.

### 10. Project Status
Local backend development, PostgreSQL integration, ETL loading, analytics APIs, dashboard API and API testing completed.

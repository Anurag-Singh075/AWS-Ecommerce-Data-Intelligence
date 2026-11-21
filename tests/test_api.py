import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_info(client):
    response = client.get("/api/v1")
    assert response.status_code == 200


def test_database_health(client):
    response = client.get("/api/v1/health/database")
    assert response.status_code == 200


def test_all_api_routes_registered():
    paths = app.openapi()["paths"]

    expected_routes = [
        "/api/v1/customers/",
        "/api/v1/orders/",
        "/api/v1/order-items/",
        "/api/v1/products/",
        "/api/v1/sellers/",
        "/api/v1/payments/",
        "/api/v1/reviews/",
        "/api/v1/geolocations/",
        "/api/v1/categories/",
        "/api/v1/analytics/overview",
        "/api/v1/analytics/order-status",
        "/api/v1/analytics/payments",
        "/api/v1/analytics/reviews",
        "/api/v1/analytics/monthly-sales",
        "/api/v1/analytics/top-products",
        "/api/v1/analytics/top-categories",
        "/api/v1/analytics/customers",
        "/api/v1/analytics/seller-performance",
        "/api/v1/dashboard/"
    ]

    for route in expected_routes:
        assert route in paths


def test_security_headers(client):
    response = client.get("/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Referrer-Policy" in response.headers
    assert "Permissions-Policy" in response.headers

@pytest.mark.parametrize(
    "endpoint",
    [
        "/api/v1/customers/",
        "/api/v1/orders/",
        "/api/v1/order-items/",
        "/api/v1/products/",
        "/api/v1/sellers/",
        "/api/v1/payments/",
        "/api/v1/reviews/",
        "/api/v1/geolocations/",
        "/api/v1/categories/",
        "/api/v1/analytics/overview",
        "/api/v1/analytics/order-status",
        "/api/v1/analytics/payments",
        "/api/v1/analytics/reviews",
        "/api/v1/analytics/monthly-sales",
        "/api/v1/analytics/top-products",
        "/api/v1/analytics/top-categories",
        "/api/v1/analytics/customers",
        "/api/v1/analytics/seller-performance",
        "/api/v1/dashboard/"
    ]
)
def test_get_api_endpoints(client, endpoint):
    response = client.get(endpoint)

    assert response.status_code == 200, (
        f"{endpoint} failed: "
        f"Status={response.status_code}, "
        f"Response={response.text[:500]}"
    )
import pytest
from fastapi.testclient import TestClient
from app.api.main import app
import json

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_predict_country():
    response = client.get("/predict/US")
    assert response.status_code == 200
    assert "country" in response.json()
    assert "predicted_revenue" in response.json()

def test_predict_all():
    response = client.get("/predict/all")
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert isinstance(response.json()["predictions"], list)

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "predictions_count" in response.json()
    assert "average_response_time" in response.json()
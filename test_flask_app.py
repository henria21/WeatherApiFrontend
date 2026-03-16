import pytest
from unittest.mock import patch, MagicMock
import requests

from flask_app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --- /health ---

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


# --- /api/cities ---

def test_get_cities(client):
    response = client.get("/api/cities")
    assert response.status_code == 200
    data = response.get_json()
    assert "cities" in data
    assert isinstance(data["cities"], list)


# --- /api/weather ---

def test_weather_missing_city(client):
    response = client.get("/api/weather")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_weather_empty_city(client):
    response = client.get("/api/weather?city=")
    assert response.status_code == 400


def test_weather_city_too_long(client):
    response = client.get("/api/weather?city=" + "a" * 101)
    assert response.status_code == 400
    assert "too long" in response.get_json()["error"]


def test_weather_success(client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"temperature": 20, "city": "London"}

    with patch("flask_app.requests.get", return_value=mock_response):
        response = client.get("/api/weather?city=London")

    assert response.status_code == 200
    assert response.get_json()["city"] == "London"


def test_weather_backend_error(client):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"detail": "City not found"}

    with patch("flask_app.requests.get", return_value=mock_response):
        response = client.get("/api/weather?city=Unknown")

    assert response.status_code == 404
    assert response.get_json()["error"] == "City not found"


def test_weather_backend_timeout(client):
    with patch("flask_app.requests.get", side_effect=requests.exceptions.Timeout):
        response = client.get("/api/weather?city=London")

    assert response.status_code == 503
    assert "timed out" in response.get_json()["error"]


def test_weather_backend_unavailable(client):
    with patch("flask_app.requests.get", side_effect=requests.exceptions.ConnectionError):
        response = client.get("/api/weather?city=London")

    assert response.status_code == 503
    assert "unavailable" in response.get_json()["error"]

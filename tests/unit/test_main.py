import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError, DatabaseError
from unittest.mock import patch, MagicMock

from services.backend.src.main import app

client = TestClient(app)

def test_root_endpoint():
    with patch("services.backend.src.wildbook.Wildbook.is_running", return_value=True):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "message": "Hello Seals!",
            "wildbook": True,
        }

def test_sqlalchemy_exception_handler():
    response = client.get("/raise-sqlalchemy-error")
    assert response.status_code == 500
    assert response.json() == {
        "message": "An internal server error occurred.",
        "error": "SQLAlchemy error"
    }

def test_integrity_error_handler():
    response = client.get("/raise-integrity-error")
    assert response.status_code == 400
    assert "Integrity error" in response.json()["error"]
    assert response.json()["message"] == "Integrity error occurred."

def test_data_error_handler():
    response = client.get("/raise-data-error")
    assert response.status_code == 400
    assert "Data error" in response.json()["error"]
    assert response.json()["message"] == "Data error occurred."

def test_database_error_handler():
    response = client.get("/raise-database-error")
    assert response.status_code == 500
    assert "Database error" in response.json()["error"]
    assert response.json()["message"] == "Database error occurred."
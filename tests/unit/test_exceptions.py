import pytest
import json
from fastapi.responses import JSONResponse
from services.backend.src.exceptions import (
    sqlalchemy_exception_handler,
    sqlalchemy_integrity_error_handler,
    sqlalchemy_data_error_handler,
    sqlalchemy_database_error_handler,
)

def test_sqlalchemy_exception_handler():
    class TestException(Exception):
        pass
    
    exc = TestException("Test error")
    response = sqlalchemy_exception_handler(None, exc)
    
    assert response.status_code == 500
    assert json.loads(response.body) == {
        "message": "An internal server error occurred.",
        "error": "Test error"
    }

def test_sqlalchemy_integrity_error_handler():
    class IntegrityError(Exception):
        pass
    
    exc = IntegrityError("Integrity error")
    response = sqlalchemy_integrity_error_handler(None, exc)
    
    assert response.status_code == 400
    assert json.loads(response.body) == {
        "message": "Integrity error occurred.",
        "error": "Integrity error"
    }

def test_sqlalchemy_data_error_handler():
    class DataError(Exception):
        pass
    
    exc = DataError("Data error")
    response = sqlalchemy_data_error_handler(None, exc)
    
    assert response.status_code == 400
    assert json.loads(response.body) == {
        "message": "Data error occurred.",
        "error": "Data error"
    }

def test_sqlalchemy_database_error_handler():
    class DatabaseError(Exception):
        pass
    
    exc = DatabaseError("Database error")
    response = sqlalchemy_database_error_handler(None, exc)
    
    assert response.status_code == 500
    assert json.loads(response.body) == {
        "message": "Database error occurred.",
        "error": "Database error"
    }
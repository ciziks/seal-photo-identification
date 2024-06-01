from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.backend.src.main import app, get_db
from services.backend.src.endpoints.seals import Seal
from services.backend.src.database import Base
from services.backend.src.models import Seal
from services.backend.src.wildbook import Wildbook
import pytest
import requests_mock

API_URL = "http://wildbook:5000/api"

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Mock the requests module
@pytest.fixture
def mock_requests(monkeypatch):
    with requests_mock.Mocker() as m:
        yield m

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
wildbook = Wildbook()

def test_create_seal():
    seal_data = {
        "ID": "1",
        "age": "adult",
        "description": "Large grey seal",
        "gender": "Male",
        "isPregnant": "No"
    }
    response = client.post("/seal", json=seal_data)
    assert response.status_code == 200, f"Failed with message: {response.json()}"
    data = response.json()
    assert data["ID"] == "1"
  
def test_read_seal():
    db = next(override_get_db())
    db.add(Seal(ID="S001", age="pup", gender="Male", description="Large seal", isPregnant="No"))
    db.commit()
    response = client.get("/seals/S001")
    assert response.status_code == 200
    assert response.json()["ID"] == "S001"

def test_list_seals():
    response = client.get("/seals")
    assert response.status_code == 200
    assert type(response.json()["data"]) == dict

def test_update_seal():    
    update_data = {
        "age": "6",
        "description": "Very large seal",
        "gender": "Male",
        "isPregnant": "No"
    }
    response = client.put("/seals/S001", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["age"] == "6"

def test_delete_seal():
    response = client.delete("/seals/S001")
    assert response.status_code == 200
    assert "ID" in response.json()

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    pytest.main()

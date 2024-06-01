from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.backend.src.main import app, get_db
from services.backend.src.endpoints.seals import create_seal
from services.backend.src.database import Base
from services.backend.src.models import Seal
from services.backend.src.crud.seal import SealCRUD
from services.backend.src.schemas import SealCreate
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

def test_create_seal_db():
    

def test_create_seal_db():
    wildbook = Wildbook()
    
    
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    pytest.main()
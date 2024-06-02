import pytest, requests_mock
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from services.backend.src.main import app
from services.backend.src.constants import (
    SEAL_NOT_FOUND_MESSAGE,
    SEAL_ALREADY_EXISTS_MESSAGE
)
from services.backend.src.schemas import Seal, SealCreate

client = TestClient(app)

@pytest.fixture
def mock_wildbook():
    with patch("services.backend.src.wildbook.Wildbook") as MockWildbook:
        mock_wildbook = MockWildbook.return_value
        yield mock_wildbook

@pytest.fixture
def mock_seal_dao():
    with patch("services.backend.src.crud.seal.SealDAO") as MockSealDAO:
        mock_seal_dao = MockSealDAO.return_value
        yield mock_seal_dao

@pytest.fixture
def mock_sighting_dao():
    with patch("services.backend.src.crud.sighting.SightingDAO") as MockSightingDAO:
        mock_sighting_dao = MockSightingDAO.return_value
        yield mock_sighting_dao

@pytest.fixture
def seal_data():
    return {
        "ID": "seal_123",
        "age": "adult",
        "description": "A seal",
        "gender": "male",
        "isPregnant": None,
        "encounters": []
    }


def test_create_seal(mock_seal_dao, seal_data):
    mock_seal_dao.get_seal.return_value = None
    mock_seal_dao.create_seal.return_value = Seal(**seal_data)
    
    response = client.post("/seals", json=seal_data)
    
    assert response.status_code == 200
    assert response.json()["ID"] == "seal_123"
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")
    mock_seal_dao.create_seal.assert_called_once_with(seal=SealCreate(**seal_data))

def test_create_seal_already_exists(mock_seal_dao, seal_data):
    mock_seal_dao.get_seal.return_value = Seal(**seal_data)
    
    response = client.post("/seals", json=seal_data)
    
    assert response.status_code == 400
    assert response.json() == {"detail": SEAL_ALREADY_EXISTS_MESSAGE}
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")

def test_read_seal(mock_seal_dao, mock_sighting_dao, mock_wildbook, seal_data):
    mock_seal_dao.get_seal.return_value = Seal(**seal_data)
    mock_wildbook.get_annotation_image.return_value = "image_url"
    mock_sighting_dao.get_sighting_from_id.return_value = MagicMock(Date="2022-01-01T00:00:00", Location="Beach")
    
    response = client.get("/seals/seal_123")
    
    assert response.status_code == 200
    assert response.json()["ID"] == "seal_123"
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")
    mock_wildbook.get_annotation_image.assert_called_once()
    mock_sighting_dao.get_sighting_from_id.assert_called_once()

def test_read_seal_not_found(mock_seal_dao):
    mock_seal_dao.get_seal.return_value = None
    
    response = client.get("/seals/seal_123")
    
    assert response.status_code == 404
    assert response.json() == {"detail": SEAL_NOT_FOUND_MESSAGE}
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")

def test_list_seals_with_pagination(mock_seal_dao, mock_wildbook, seal_data):
    mock_seal_dao.list_seals.return_value = (1, [Seal(**seal_data)])
    mock_wildbook.get_annotation_image.return_value = "image_url"
    
    response = client.get("/seals")
    
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["limit"] == 10
    assert response.json()["skip"] == 0
    assert "seal_123" in response.json()["data"]
    mock_seal_dao.list_seals.assert_called_once_with(skip=0, limit=10)
    mock_wildbook.get_annotation_image.assert_called_once()

def test_update_seal(mock_seal_dao, seal_data):
    mock_seal_dao.get_seal.return_value = Seal(**seal_data)
    mock_seal_dao.update_seal.return_value = Seal(**seal_data)
    
    response = client.put("/seals/seal_123", json=seal_data)
    
    assert response.status_code == 200
    assert response.json()["ID"] == "seal_123"
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")
    mock_seal_dao.update_seal.assert_called_once_with(db_seal=Seal(**seal_data), seal=SealCreate(**seal_data))

def test_update_seal_not_found(mock_seal_dao, seal_data):
    mock_seal_dao.get_seal.return_value = None
    
    response = client.put("/seals/seal_123", json=seal_data)
    
    assert response.status_code == 404
    assert response.json() == {"detail": SEAL_NOT_FOUND_MESSAGE}
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")

def test_delete_seal(mock_seal_dao, seal_data):
    mock_seal_dao.get_seal.return_value = Seal(**seal_data)
    mock_seal_dao.delete_seal.return_value = Seal(**seal_data)
    
    response = client.delete("/seals/seal_123")
    
    assert response.status_code == 200
    assert response.json()["ID"] == "seal_123"
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")
    mock_seal_dao.delete_seal.assert_called_once_with(seal=Seal(**seal_data))

def test_delete_seal_not_found(mock_seal_dao):
    mock_seal_dao.get_seal.return_value = None
    
    response = client.delete("/seals/seal_123")
    
    assert response.status_code == 404
    assert response.json() == {"detail": SEAL_NOT_FOUND_MESSAGE}
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")
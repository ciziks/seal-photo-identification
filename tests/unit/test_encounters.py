import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from services.backend.src.main import app
from services.backend.src.constants import (
    SIGHTING_NOT_FOUND_MESSAGE,
    SEAL_NOT_FOUND_MESSAGE
)
from services.backend.src.schemas import EncounterSchema, EncounterCreate

client = TestClient(app)

@pytest.fixture
def mock_encounter_dao():
    with patch("services.backend.src.crud.encounter.EncounterDAO") as MockEncounterDAO:
        mock_encounter_dao = MockEncounterDAO.return_value
        yield mock_encounter_dao

@pytest.fixture
def mock_sighting_dao():
    with patch("services.backend.src.crud.sighting.SightingDAO") as MockSightingDAO:
        mock_sighting_dao = MockSightingDAO.return_value
        yield mock_sighting_dao

@pytest.fixture
def mock_seal_dao():
    with patch("services.backend.src.crud.seal.SealDAO") as MockSealDAO:
        mock_seal_dao = MockSealDAO.return_value
        yield mock_seal_dao

@pytest.fixture
def encounter_data():
    return {
        "SightingID": 1,
        "SealID": "seal_123",
        "WildBookID": 456
    }

def test_create_encounter(mock_encounter_dao, mock_sighting_dao, mock_seal_dao, encounter_data):
    mock_sighting_dao.get_sighting_from_id.return_value = MagicMock()
    mock_seal_dao.get_seal.return_value = MagicMock()
    mock_encounter_dao.create_encounter.return_value = EncounterSchema(**encounter_data)
    
    response = client.post("/encounters", json=encounter_data)
    
    assert response.status_code == 200
    assert response.json()["SightingID"] == 1
    assert response.json()["SealID"] == "seal_123"
    assert response.json()["WildBookID"] == 456
    mock_sighting_dao.get_sighting_from_id.assert_called_once_with(sighting_id=1)
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")
    mock_encounter_dao.create_encounter.assert_called_once_with(encounter=EncounterCreate(**encounter_data))

def test_create_encounter_sighting_not_found(mock_encounter_dao, mock_sighting_dao, mock_seal_dao, encounter_data):
    mock_sighting_dao.get_sighting_from_id.return_value = None
    mock_seal_dao.get_seal.return_value = MagicMock()
    
    response = client.post("/encounters", json=encounter_data)
    
    assert response.status_code == 404
    assert response.json() == {"detail": SIGHTING_NOT_FOUND_MESSAGE}
    mock_sighting_dao.get_sighting_from_id.assert_called_once_with(sighting_id=1)
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")
    mock_encounter_dao.create_encounter.assert_not_called()

def test_create_encounter_seal_not_found(mock_encounter_dao, mock_sighting_dao, mock_seal_dao, encounter_data):
    mock_sighting_dao.get_sighting_from_id.return_value = MagicMock()
    mock_seal_dao.get_seal.return_value = None
    
    response = client.post("/encounters", json=encounter_data)
    
    assert response.status_code == 404
    assert response.json() == {"detail": SEAL_NOT_FOUND_MESSAGE}
    mock_sighting_dao.get_sighting_from_id.assert_called_once_with(sighting_id=1)
    mock_seal_dao.get_seal.assert_called_once_with(seal_id="seal_123")
    mock_encounter_dao.create_encounter.assert_not_called()
import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from services.backend.src.models import Encounter
from services.backend.src.schemas import EncounterCreate
from services.backend.src.database import get_db
from services.backend.src.crud.encounter import EncounterDAO

@pytest.fixture
def mock_db_session():
    with patch("services.backend.src.crud.encounter.get_db") as mock_get_db:
        mock_session = MagicMock(spec=Session)
        mock_get_db.return_value = mock_session
        yield mock_session

@pytest.fixture
def encounter_data():
    return {
        "EncounterID": 1,
        "SightingID": 1,
        "SealID": "seal_123",
        "WildBookID": 456
    }

def test_create_encounter(mock_db_session, encounter_data):
    encounter_create = EncounterCreate(**encounter_data)
    mock_db_session.add.side_effect = lambda x: setattr(x, 'EncounterID', 1)  # Mock the ID assignment
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda x: x  # Mock refresh to return the same object
    
    encounter_dao = EncounterDAO(mock_db_session)
    
    new_encounter = encounter_dao.create_encounter(encounter_create)
    
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert new_encounter.EncounterID == 1
    assert new_encounter.SightingID == 1
    assert new_encounter.SealID == "seal_123"
    assert new_encounter.WildBookID == 456

def test_get_encounter(mock_db_session, encounter_data):
    encounter = MagicMock(spec=Encounter)
    encounter.EncounterID = encounter_data["EncounterID"]
    encounter.SightingID = encounter_data["SightingID"]
    encounter.SealID = encounter_data["SealID"]
    encounter.WildBookID = encounter_data["WildBookID"]

    mock_db_session.query.return_value.filter.return_value.first.return_value = encounter
    
    encounter_dao = EncounterDAO(mock_db_session)
    
    result = encounter_dao.get_encounter(1)
    
    assert result.EncounterID == 1
    assert result.SightingID == 1
    assert result.SealID == "seal_123"
    assert result.WildBookID == 456
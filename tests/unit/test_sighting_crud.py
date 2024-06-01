import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from datetime import datetime
from services.backend.src.models import Sighting
from services.backend.src.schemas import SightingCreate
from services.backend.src.database import get_db
from services.backend.src.crud.sighting import SightingDAO

@pytest.fixture
def mock_db_session():
    with patch("services.backend.src.database.get_db") as mock_get_db:
        mock_session = MagicMock(spec=Session)
        mock_get_db.return_value = mock_session
        yield mock_session

@pytest.fixture
def sighting_data():
    return {
        "SightingID": 1,
        "Date": datetime(2022, 1, 1),
        "Location": "Beach"
    }

def test_get_sighting_from_id(mock_db_session, sighting_data):
    mock_db_session.query.return_value.filter.return_value.options.return_value.first.return_value = Sighting(**sighting_data)
    sighting_dao = SightingDAO(mock_db_session)
    
    result = sighting_dao.get_sighting_from_id(1)
    
    assert result.SightingID == 1
    assert result.Date == datetime(2022, 1, 1)
    assert result.Location == "Beach"

def test_find_sighting(mock_db_session, sighting_data):
    sighting_instance = Sighting(**sighting_data)
    mock_db_session.query.return_value.options.return_value.filter.return_value.all.return_value = [sighting_instance]
    sighting_dao = SightingDAO(mock_db_session)
    
    results = sighting_dao.find_sighting(date=datetime(2022, 1, 1), location="Beach")
    
    #assert len(results) == 1
    #assert results[0].SightingID == 1

def test_list_sightings(mock_db_session, sighting_data):
    sighting_instance = Sighting(**sighting_data)
    mock_db_session.query.return_value.options.return_value.offset.return_value.limit.return_value.all.return_value = [sighting_instance]
    mock_db_session.query.return_value.options.return_value.count.return_value = 1
    sighting_dao = SightingDAO(mock_db_session)
    
    total, sightings = sighting_dao.list_sightings(skip=0, limit=10)
    
    assert total == 1
    assert len(sightings) == 1
    assert sightings[0].SightingID == 1

def test_create_sighting(mock_db_session, sighting_data):
    sighting_create = SightingCreate(**sighting_data)
    mock_db_session.add.side_effect = lambda x: setattr(x, 'SightingID', 1)  # Mock the ID assignment
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda x: x  # Mock refresh to return the same object
    
    sighting_dao = SightingDAO(mock_db_session)
    
    new_sighting = sighting_dao.create_sighting(sighting_create)
    
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert new_sighting.SightingID == 1

def test_update_sighting(mock_db_session, sighting_data):
    sighting_instance = Sighting(**sighting_data)
    updated_data = sighting_data.copy()
    updated_data["Location"] = "Harbor"
    sighting_update = SightingCreate(**updated_data)
    
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None
    sighting_dao = SightingDAO(mock_db_session)
    
    updated_sighting = sighting_dao.update_sighting(sighting_instance, sighting_update)
    
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert updated_sighting.Location == "Harbor"

def test_delete_sighting(mock_db_session, sighting_data):
    sighting_instance = Sighting(**sighting_data)
    
    mock_db_session.commit.return_value = None
    sighting_dao = SightingDAO(mock_db_session)
    
    deleted_sighting = sighting_dao.delete_sighting(sighting_instance)
    
    mock_db_session.delete.assert_called_once_with(sighting_instance)
    mock_db_session.commit.assert_called_once()
    assert deleted_sighting == sighting_instance
import pytest, os, sys
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from services.backend.src.models import Seal
from services.backend.src.schemas import SealCreate
from services.backend.src.database import get_db
from services.backend.src.crud.seal import SealDAO

@pytest.fixture
def mock_db_session():
    with patch("services.backend.src.database.get_db") as mock_get_db:
        mock_session = MagicMock(spec=Session)
        mock_get_db.return_value = mock_session
        yield mock_session

@pytest.fixture
def seal_data():
    return {
        "ID": "seal_123",
        "age": "5",
        "description": "A description",
        "gender": "female",
        "isPregnant": "no"
    }

def test_get_seal(mock_db_session, seal_data):
    mock_db_session.query.return_value.filter.return_value.options.return_value.first.return_value = Seal(**seal_data)
    seal_dao = SealDAO(mock_db_session)
    
    result = seal_dao.get_seal("seal_123")
    
    assert result.ID == "seal_123"
    assert result.age == "5"
    assert result.description == "A description"
    assert result.gender == "female"
    assert result.isPregnant == "no"

def test_list_seals(mock_db_session, seal_data):
    seal_instance = Seal(**seal_data)
    mock_db_session.query.return_value.options.return_value.offset.return_value.limit.return_value.all.return_value = [seal_instance]
    mock_db_session.query.return_value.options.return_value.count.return_value = 1
    seal_dao = SealDAO(mock_db_session)
    
    total, seals = seal_dao.list_seals(skip=0, limit=10)
    
    assert total == 1
    assert len(seals) == 1
    assert seals[0].ID == "seal_123"

def test_create_seal(mock_db_session, seal_data):
    seal_create = SealCreate(**seal_data)
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    seal_dao = SealDAO(mock_db_session)
    
    new_seal = seal_dao.create_seal(seal_create)
    
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert new_seal.ID == "seal_123"

def test_update_seal(mock_db_session, seal_data):
    seal_instance = Seal(**seal_data)
    updated_data = seal_data.copy()
    updated_data["age"] = "6"
    seal_update = SealCreate(**updated_data)
    
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None
    seal_dao = SealDAO(mock_db_session)
    
    updated_seal = seal_dao.update_seal(seal_instance, seal_update)
    
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert updated_seal.age == "6"

def test_delete_seal(mock_db_session, seal_data):
    seal_instance = Seal(**seal_data)
    
    mock_db_session.commit.return_value = None
    seal_dao = SealDAO(mock_db_session)
    
    deleted_seal = seal_dao.delete_seal(seal_instance)
    
    mock_db_session.delete.assert_called_once_with(seal_instance)
    mock_db_session.commit.assert_called_once()
    assert deleted_seal == seal_instance
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from services.backend.src.main import app
from services.backend.src.constants import (
    SIGHTING_NOT_FOUND_MESSAGE,
    INVALID_DATE_MESSAGE
)
from services.backend.src.schemas import SightingCreate, Sighting

client = TestClient(app)

@pytest.fixture
def mock_wildbook():
    with patch("services.backend.src.wildbook.Wildbook") as MockWildbook:
        mock_wildbook = MockWildbook.return_value
        yield mock_wildbook

@pytest.fixture
def mock_sighting_dao():
    with patch("services.backend.src.crud.sighting.SightingDAO") as MockSightingDAO:
        mock_sighting_dao = MockSightingDAO.return_value
        yield mock_sighting_dao

@pytest.fixture
def sighting_data():
    return {
        "SightingID": 1,
        "Date": "2022-01-01T00:00:00",
        "Location": "Center",
        "encounters": []
    }

def test_create_sighting(mock_sighting_dao, sighting_data):
    mock_sighting_dao.find_sighting.return_value = []
    mock_sighting_dao.create_sighting.return_value = Sighting(**sighting_data)
    
    SightingCreate(**{
        "Date": datetime.strptime(sighting_data["Date"], "%Y-%m-%dT%H:%M:%S"),
        "Location": sighting_data["Location"],
        "encounters": sighting_data["encounters"]
    })
    response = client.post("/sightings", json={
        "Date": "01-01-2022",
        "Location": "Center",
        "encounters": []
    })
    
    assert response.status_code == 200
    assert response.json()["SightingID"] == 1
    assert response.json()["Date"] == "2022-01-01T00:00:00"
    assert response.json()["Location"] == "Center"

def test_read_sighting(mock_sighting_dao, mock_wildbook, sighting_data):
    mock_sighting_dao.get_sighting_from_id.return_value = Sighting(**sighting_data)
    mock_wildbook.get_annotation_image.return_value = "image_url"
    
    response = client.get("/sightings/1")
    
    assert response.status_code == 200
    assert response.json()["SightingID"] == 1
    assert response.json()["Date"] == "2022-01-01T00:00:00"
    assert response.json()["Location"] == "Center"
    assert response.json()["images"] == ["image_url"]

def test_list_sightings(mock_sighting_dao, mock_wildbook, sighting_data):
    mock_sighting_dao.list_sightings.return_value = (1, [Sighting(**sighting_data)])
    mock_wildbook.get_annotation_image.return_value = "image_url"
    
    response = client.get("/sightings")
    
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["limit"] == 10
    assert response.json()["skip"] == 0
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["SightingID"] == 1
    assert response.json()["data"][0]["images"] == ["image_url"]

def test_update_sighting(mock_sighting_dao, sighting_data):
    mock_sighting_dao.get_sighting_from_id.return_value = Sighting(**sighting_data)
    mock_sighting_dao.update_sighting.return_value = Sighting(**sighting_data)
    
    SightingCreate(**{
        "Date": datetime.strptime(sighting_data["Date"], "%Y-%m-%dT%H:%M:%S"),
        "Location": sighting_data["Location"],
        "encounters": sighting_data["encounters"]
    })
    response = client.put("/sightings/1", json={
        "Date": "01-01-2022",
        "Location": "Center",
        "encounters": []
    })
    
    assert response.status_code == 200
    assert response.json()["SightingID"] == 1
    assert response.json()["Date"] == "2022-01-01T00:00:00"
    assert response.json()["Location"] == "Center"

def test_delete_sighting(mock_sighting_dao, sighting_data):
    mock_sighting_dao.get_sighting_from_id.return_value = Sighting(**sighting_data)
    mock_sighting_dao.delete_sighting.return_value = Sighting(**sighting_data)
    
    response = client.delete("/sightings/1")
    
    assert response.status_code == 200
    assert response.json()["SightingID"] == 1
    assert response.json()["Date"] == "2022-01-01T00:00:00"
    assert response.json()["Location"] == "Center"

def test_delete_sighting_by_date_location(mock_sighting_dao, sighting_data):
    mock_sighting_dao.find_sighting.return_value = [Sighting(**sighting_data)]
    mock_sighting_dao.delete_sighting.return_value = Sighting(**sighting_data)
    
    response = client.delete("/sightings/Center/01-01-2022")
    
    assert response.status_code == 200
    assert response.json()["SightingID"] == 1
    assert response.json()["Date"] == "2022-01-01T00:00:00"
    assert response.json()["Location"] == "Center"

def test_search_sightings(mock_sighting_dao, mock_wildbook, sighting_data):
    mock_sighting_dao.find_sighting.return_value = [Sighting(**sighting_data)]
    mock_wildbook.get_annotation_image.return_value = "image_url"
    
    response = client.get("/sightings/search/?date=01-01-2022&location=Center")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["SightingID"] == 1
    assert response.json()[0]["images"] == ["image_url"]

def test_invalid_date(mock_sighting_dao):
    response = client.get("/sightings/search/?date=invalid-date&location=Center")
    
    assert response.status_code == 400
    assert response.json() == {"detail": INVALID_DATE_MESSAGE}

def test_sighting_not_found(mock_sighting_dao):
    mock_sighting_dao.get_sighting_from_id.return_value = None
    
    response = client.get("/sightings/1")
    
    assert response.status_code == 404
    assert response.json() == {"detail": SIGHTING_NOT_FOUND_MESSAGE}
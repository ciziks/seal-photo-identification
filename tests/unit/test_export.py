import os, sys
from fastapi import FastAPI
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from services.backend.src.endpoints.export import router, export_data
from services.backend.src.database import get_db
from services.backend.src.models import Sighting, Seal, Encounter

app = FastAPI()
app.include_router(router, prefix="/export")

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    with patch("services.backend.src.database.get_db") as mock_get_db:
        mock_session = MagicMock(spec=Session)
        mock_get_db.return_value = mock_session
        yield mock_session

@pytest.fixture
def mock_data():
    sightings_data = pd.DataFrame({
        "SightingID": [1, 2],
        "Date": ["01-01-2024", "31-12-2023"],
        "Location": ["Beach", "Harbor"]
    })
    seals_data = pd.DataFrame({
        "ID": [101, 102],
        "SealID": [1, 2],
        "Name": ["SealA", "SealB"]
    })
    encounters_data = pd.DataFrame({
        "EncounterID": [1, 2],
        "SightingID": [1, 2],
        "SealID": [101, 102]
    })
    return sightings_data, seals_data, encounters_data

@pytest.fixture()
def mock_no_data():
    sightings_data = pd.DataFrame({
        "SightingID": [],
        "Date": [],
        "Location": []
    })
    seals_data = pd.DataFrame({
        "ID": [],
        "SealID": [],
        "Name": []
    })
    encounters_data = pd.DataFrame({
        "EncounterID": [],
        "SightingID": [],
        "SealID": []
    })
    return sightings_data, seals_data, encounters_data

def test_export_data(mock_db_session, mock_data):
    sightings_data, seals_data, encounters_data = mock_data

    # Mock the SQL query responses
    mock_db_session.query.return_value.statement = None
    with patch("pandas.read_sql", side_effect=[sightings_data, seals_data, encounters_data]):
        response = client.get("/export")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    # Ensure the file is created
    assert os.path.exists("sealcenter_data.xlsx")
    os.remove("sealcenter_data.xlsx")  # Clean up

def test_export_data_no_data(mock_db_session, mock_no_data):
    sightings_data, seals_data, encounters_data = mock_no_data
    # Mock empty dataframes for SQL query responses
    with patch("pandas.read_sql", side_effect=[sightings_data, seals_data, encounters_data]):
        response = client.get("/export")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    # Ensure the file is created
    assert os.path.exists("sealcenter_data.xlsx")
    os.remove("sealcenter_data.xlsx")  # Clean up
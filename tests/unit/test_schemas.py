import pytest
from pydantic import ValidationError
from datetime import datetime
from services.backend.src.schemas import (
    EncounterSchema,
    SealSchema,
    SightingCreate,
    Sighting
)

def test_encounter_schema():
    encounter_data = {
        "SightingID": 1,
        "SealID": "seal_123",
        "WildBookID": 456
    }
    encounter = EncounterSchema(**encounter_data)
    assert encounter.SightingID == 1
    assert encounter.SealID == "seal_123"
    assert encounter.WildBookID == 456

def test_seal_schema():
    seal_data = {
        "ID": "seal_123",
        "age": "5",
        "description": "A description",
        "gender": "female",
        "isPregnant": "no"
    }
    seal = SealSchema(**seal_data)
    assert seal.ID == "seal_123"
    assert seal.age == "5"
    assert seal.description == "A description"
    assert seal.gender == "female"
    assert seal.isPregnant == "no"

def test_sighting_create_schema():
    sighting_data = {
        "Date": "01/01/2022",
        "Location": "Beach"
    }
    sighting = SightingCreate(**sighting_data)
    assert sighting.Date == datetime(2022, 1, 1)
    assert sighting.Location == "Beach"

def test_sighting_create_schema_invalid_date():
    sighting_data = {
        "Date": "invalid_date",
        "Location": "Beach"
    }
    with pytest.raises(ValidationError):
        SightingCreate(**sighting_data)

def test_sighting_schema():
    sighting_data = {
        "Date": datetime(2022, 1, 1),
        "Location": "Beach",
        "SightingID": 1,
        "encounters": [],
        "images": []
    }
    sighting = Sighting(**sighting_data)
    assert sighting.Date == datetime(2022, 1, 1)
    assert sighting.Location == "Beach"
    assert sighting.SightingID == 1
    assert sighting.encounters == []
    assert sighting.images == []
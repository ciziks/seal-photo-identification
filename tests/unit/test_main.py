import pytest
from fastapi.testclient import TestClient
from services.backend.src.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200

    expected_response = {
        "text": "Hello World",
        "wildbook": True,
    }
    response_json = response.json()

    assert response_json["text"] == expected_response["text"]
    assert response_json["wildbook"] == expected_response["wildbook"]

    db_result = response_json["db"]
    if isinstance(db_result, dict):
        assert "ID" in db_result
        assert "age" in db_result
        assert "comments" in db_result
        assert "gender" in db_result
        assert "ispregnant" in db_result
    else:
        assert db_result == "No data found"

def test_new_seal_not_registered_endpoint():
    new_seal_data = {
        "ID": "new_seal_id",
        "age": "adult",
        "comments": "This is a new seal",
        "gender": "male",
        "isPregnant": "false"
    }

    response = client.post("/seal", json=new_seal_data)
    assert response.status_code == 200
    assert response.json()["ID"] == "new_seal_id"
    assert response.json()["age"] == "adult"
    assert response.json()["comments"] == "This is a new seal"
    assert response.json()["gender"] == "male"
    assert response.json()["isPregnant"] == "false"


def test_new_seal_registered_endpoint():
    new_seal_data = {
        "ID": "new_seal_id",
        "age": "adult",
        "comments": "This is a new seal",
        "gender": "male",
        "isPregnant": "false"
    }

    response = client.post("/seal", json=new_seal_data)
    assert response.status_code == 400
    assert "Seal already registered" in response.text

def test_read_seal_not_found_endpoint():
    response = client.post("/seals/{seal_id}")
    assert response.status_code == 404
    assert "Seal not found" in response.text

def test_read_seal_found_endpoint():
    response = client.get("/seals/{seal_id}")
    assert response.status_code == 200

    response_json = response.json()
    images = response_json["images"]

    assert "ID" in response_json
    assert "age" in response_json
    assert "comments" in response_json
    assert "gender" in response_json
    assert "ispregnant" in response_json

    for image_id in images:
        assert isinstance(image_id, int)










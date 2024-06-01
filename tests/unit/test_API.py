import unittest
import requests_mock, requests
from unittest.mock import call, patch, mock_open
from services.backend.src.wildbook import Wildbook
import pytest

API_URL = "http://wildbook:5000/api"

# Mock the requests module
@pytest.fixture
def mock_requests(monkeypatch):
    with requests_mock.Mocker() as mock_get:
        yield mock_get

def test_is_running(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.get(f"{API_URL}/test/helloworld/", json={"status": {"success": True}})

    # Test the method
    assert wildbook.is_running() is True

def test_is_running_invalid_url(mock_requests):
    wildbook = Wildbook(url="http://invalidurl")
    mock_requests.get("http://invalidurl/api/test/helloworld/", exc=requests.exceptions.ConnectionError)
    assert wildbook.is_running() is False

def test_is_running_http_error(mock_requests):
    wildbook = Wildbook()
    mock_requests.get(f"{API_URL}/test/helloworld/", status_code=500)
    assert wildbook.is_running() is False

def test_upload_image(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.post(f"{API_URL}/upload/image/", json={"status": {"success": True}, "response": "image_id"})

    # Mock the open function to simulate reading a file
    with patch("builtins.open", mock_open(read_data="file_content")):
        image_id = wildbook.upload_image("dummy_path")
        assert image_id == "image_id"

def test_upload_image_invalid_path():
    wildbook = Wildbook()
    with pytest.raises(FileNotFoundError):
        wildbook.upload_image("invalid_path")

def test_get_annotation_name_key_error(mock_requests):
    wildbook = Wildbook()
    mock_requests.get(f"{API_URL}/annot/name/text/", json={"annotations": []})
    with pytest.raises(KeyError):
        wildbook.get_annotation_name("nonexistent_annotation")

def test_list_images_id_empty_response(mock_requests):
    wildbook = Wildbook()
    mock_requests.get(f"{API_URL}/image/", json={})
    assert wildbook.list_images_id() == None

def test_upload_image_file_not_found():
    wildbook = Wildbook()
    with pytest.raises(FileNotFoundError):
        wildbook.upload_image("nonexistent_file_path")

def test_seal_matching_unexpected_response(mock_requests):
    wildbook = Wildbook()
    mock_requests.get(f"{API_URL}/query/chip/dict/simple", json={"unexpected_key": []})
    with pytest.raises(KeyError):
        wildbook.seal_matching(["annotation_id"], ["comparison_id"])

def test_upload_image_failure_message(mock_requests):
    wildbook = Wildbook()
    
    # Mock the endpoint response with a failure status
    mock_requests.post(f"{API_URL}/upload/image/", json={"status": {"success": False, "message": "Failed to upload image"}})
    
    # Mock the open function to simulate reading a file
    with patch("builtins.open", mock_open(read_data="file_content")):
        result = wildbook.upload_image("dummy_path")
        
        # Test that the result is the failure message
        assert result == "Failed to upload image"

def test_remove_image(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.delete(f"{API_URL}/image/json/", json={"status": {"success": True}})

    # Test the method
    assert wildbook.remove_image(["image_uuid"]) is True

def test_list_images_id(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.get(f"{API_URL}/image/", json={"status": {"success": True}, "response": ["id1", "id2"]})

    # Test the method
    image_ids = wildbook.list_images_id()
    assert image_ids == ["id1", "id2"]

def test_get_images_size_success(mock_requests):
    wildbook = Wildbook()
    
    image_id_list = [1, 2, 3]
    
    # Mock the endpoint responses with success status and response data
    mock_requests.get(f"{API_URL}/image/height/", json={"status": True, "response": [200, 300, 400]})
    mock_requests.get(f"{API_URL}/image/width/", json={"status": True, "response": [100, 150, 200]})
    
    # Test the method
    result = wildbook.get_images_size(image_id_list)
    
    # Assert that the result is a list of tuples with width and height
    assert result == [(100, 200), (150, 300), (200, 400)]

def test_get_images_size_failure_height(mock_requests):
    wildbook = Wildbook()
    
    image_id_list = [1, 2, 3]
    
    # Mock the height endpoint response with a failure status
    mock_requests.get(f"{API_URL}/image/height/", json={"status": False, "message": "Failed to get height"})
    # Mock the width endpoint response with a success status
    mock_requests.get(f"{API_URL}/image/width/", json={"status": True, "response": [100, 150, 200]})
    
    # Test the method
    result = wildbook.get_images_size(image_id_list)
    
    # Assert that the result is an empty list when height status indicates failure
    assert result == []

def test_get_images_size_failure_width(mock_requests):
    wildbook = Wildbook()
    
    image_id_list = [1, 2, 3]
    
    # Mock the height endpoint response with a success status
    mock_requests.get(f"{API_URL}/image/height/", json={"status": True, "response": [200, 300, 400]})
    # Mock the width endpoint response with a failure status
    mock_requests.get(f"{API_URL}/image/width/", json={"status": False, "message": "Failed to get width"})
    
    # Test the method
    result = wildbook.get_images_size(image_id_list)
    
    # Assert that the result is an empty list when width status indicates failure
    assert result == []

def test_get_images_size_failure_both(mock_requests):
    wildbook = Wildbook()
    
    image_id_list = [1, 2, 3]
    
    # Mock both endpoint responses with a failure status
    mock_requests.get(f"{API_URL}/image/height/", json={"status": False, "message": "Failed to get height"})
    mock_requests.get(f"{API_URL}/image/width/", json={"status": False, "message": "Failed to get width"})
    
    # Test the method
    result = wildbook.get_images_size(image_id_list)
    
    # Assert that the result is an empty list when both statuses indicate failure
    assert result == []

def test_get_images_uuids(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.get(f"{API_URL}/image/uuid/", json={"status": {"success": True}, "response": [{"__UUID__": "uuid1"}, {"__UUID__": "uuid2"}]})

    image_ids = ["1", "2"]
    # Test the method
    image_uuids = wildbook.get_images_uuids(image_ids)
    assert image_uuids == ["uuid1", "uuid2"]

def test_create_annotations(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.post(f"{API_URL}/annot/", json={"status": {"success": True}, "response": "annot_id"})

    # Test the method
    annot_id = wildbook.create_annotations("image_id", "annot_uuid")
    assert annot_id == "annot_id"

def test_get_annotation_id(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.get(f"{API_URL}/annot/rowid/uuid", json={"status": {"success": True}, "response": "image_id"})

    # Test the method
    image_id = wildbook.get_annotation_id(["uuid"])
    assert image_id == "image_id"

def test_list_names_id(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.get(f"{API_URL}/name/", json={"status": {"success": True}, "response": ["name1", "name2"]})

    # Test the method
    names = wildbook.list_names_id()
    assert names == ["name1", "name2"]

def test_list_annotation_from_names(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.get(f"{API_URL}/name/annot/rowid/", json={"status": {"success": True}, "response": ["annot1", "annot2"]})

    # Test the method
    annotations = wildbook.list_annotation_from_names(["name1", "name2"])
    assert annotations == [1, 2]

def mock_get_annotation_id(self, uuid_list):
    return ["annot" + uuid[-1] for uuid in uuid_list]

def test_list_annotations_id(mock_requests, monkeypatch):
    wildbook = Wildbook()
    monkeypatch.setattr(wildbook, 'get_annotation_id', mock_get_annotation_id.__get__(wildbook))

    # Mock the endpoint response
    mock_requests.get(f"{API_URL}/annot/json/", json={"status": {"success": True}, "response": [{"__UUID__": "uuid1"}, {"__UUID__": "uuid2"}]})

    # Test the method
    annotations = wildbook.list_annotations_id()
    assert annotations == ["annot1", "annot2"]

def test_get_annotation_name(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.get(f"{API_URL}/annot/name/text/", json={"status": {"success": True}, "response": "annotation_name"})

    # Test the method
    annotation_name = wildbook.get_annotation_name("annot_uuid")
    assert annotation_name == "annotation_name"[0]

def test_get_annotation_image(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.get(f"{API_URL}/annot/annot_uuid/", json={"status": {"success": True}, "response": "annotation_image"})

    # Test the method
    annotation_image = wildbook.get_annotation_image("annot_uuid")
    assert annotation_image == "annotation_image"

def test_detect_seal(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.put(f"{API_URL}/detect/cnn/yolo/", json={"status": {"success": True}, "response": ["annot1", "annot2"]})

    # Test the method
    with patch("builtins.open", mock_open(read_data=b"file_content")):
        annotations = wildbook.detect_seal("dummy_path")
        assert annotations == "annot1"

def test_rename_annotations(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.put(f"{API_URL}/annot/name/", json={"status": {"success": True}})

    # Test the method
    assert wildbook.rename_annotations("annot_uuid", "new_name") is True

def test_remove_annotation(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.delete(f"{API_URL}/image/json/", json={"status": {"success": True}})

    # Test the method
    assert wildbook.remove_annotation(["annot_uuid"]) is True

def test_mark_as_exemplar(mock_requests):
    wildbook = Wildbook()
    
    annot_id_list = ["annot1", "annot2", "annot3"]
    
    # Mock the endpoint response with a success status
    mock_requests.put(f"{API_URL}/annot/exemplar/", json={"status": {"success": True}})
    
    # Test the method
    result = wildbook.mark_as_exemplar(annot_id_list)
    
    # Assert that the result is True when the status indicates success
    assert result is True

def test_mark_as_exemplar_failure(mock_requests):
    wildbook = Wildbook()
    
    annot_id_list = ["annot1", "annot2", "annot3"]
    
    # Mock the endpoint response with a failure status
    mock_requests.put(f"{API_URL}/annot/exemplar/", json={"status": {"success": False}})
    
    # Test the method
    result = wildbook.mark_as_exemplar(annot_id_list)
    
    # Assert that the result is False when the status indicates failure
    assert result is False

def test_seal_matching(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    response_json = {
        "status": {"success": True},
        "response": [
            {"qaid": "comp1", "score_list": [0.8, 0.6]},
            {"qaid": "comp2", "score_list": [0.9, 0.7]}
        ]
    }
    mock_requests.get(f"{API_URL}/query/chip/dict/simple", json=response_json)

    # Mock helper methods
    with patch.object(Wildbook, 'get_annotation_name', return_value="annotation_name"), \
         patch.object(Wildbook, 'get_annotation_image', return_value="annotation_image"):
        
        scores = wildbook.seal_matching(["annot1", "annot2"], ["comp1", "comp2"])
        assert len(scores) == 2
        assert "annot1" in scores
        assert "annot2" in scores

if __name__ == "__main__":
    pytest.main()
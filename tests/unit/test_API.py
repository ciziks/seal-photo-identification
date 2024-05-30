import requests_mock
from unittest.mock import MagicMock, patch, mock_open
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

def test_upload_image(mock_requests):
    wildbook = Wildbook()

    # Mock the endpoint response
    mock_requests.post(f"{API_URL}/upload/image/", json={"status": {"success": True}, "response": "image_id"})

    # Mock the open function to simulate reading a file
    with patch("builtins.open", mock_open(read_data="file_content")):
        image_id = wildbook.upload_image("dummy_path")
        assert image_id == "image_id"

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
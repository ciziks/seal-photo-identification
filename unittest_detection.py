import os
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from services.backend.src.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.fixture
def mock_wildbook():
    with patch("src.wildbook.Wildbook") as MockWildbook:
        mock_wildbook = MockWildbook.return_value
        mock_wildbook.list_names_id.return_value = ["seal1", "seal2"]
        mock_wildbook.list_annotation_from_names.return_value = ["annotation1", "annotation2"]
        mock_wildbook.upload_image.return_value = "image_id"
        mock_wildbook.get_images_size.return_value = [[100, 200]]
        mock_wildbook.create_annotations.return_value = ["annotation_id"]
        mock_wildbook.seal_matching.return_value = {"seal1": 0.9, "seal2": 0.1}
        yield mock_wildbook

def test_seal_matching_no_images(mock_wildbook):
    response = client.post("/your_endpoint_path", files=[])
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "No images provided"}  # Replace with your actual NO_IMAGE_MESSAGE constant

def test_seal_matching_success(mock_wildbook):
    image_path = "test_image.jpg"
    with open(image_path, "wb") as f:
        f.write(os.urandom(1024))  # Creating a random file for testing

    with open(image_path, "rb") as f:
        files = {"images": (image_path, f, "image/jpeg")}
        response = client.post("/your_endpoint_path", files=files)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"seal1": 0.9, "seal2": 0.1}

    os.remove(image_path)

def test_seal_matching_temp_file_removal(mock_wildbook):
    image_path = "test_image.jpg"
    with open(image_path, "wb") as f:
        f.write(os.urandom(1024))  # Creating a random file for testing

    with open(image_path, "rb") as f:
        files = {"images": (image_path, f, "image/jpeg")}
        response = client.post("/your_endpoint_path", files=files)

    assert response.status_code == status.HTTP_200_OK

    # Ensure temporary files are removed
    temp_image_path = f"temp_{image_path}"
    assert not os.path.exists(temp_image_path)

    os.remove(image_path)
import pytest
from services.backend.src.constants import (
    SEAL_NOT_FOUND_MESSAGE,
    SEAL_ALREADY_EXISTS_MESSAGE,
    SIGHTING_NOT_FOUND_MESSAGE,
    NO_IMAGE_MESSAGE,
    INVALID_DATE_MESSAGE
)

def test_constants():
    assert SEAL_NOT_FOUND_MESSAGE == "Seal not found"
    assert SEAL_ALREADY_EXISTS_MESSAGE == "Seal already registered"
    assert SIGHTING_NOT_FOUND_MESSAGE == "Sighting not found"
    assert NO_IMAGE_MESSAGE == "No images uploaded"
    assert INVALID_DATE_MESSAGE == "Invalid date format. Use 'dd-mm-yyyy'."
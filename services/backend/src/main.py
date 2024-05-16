from typing import Union
from fastapi import FastAPI, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from .wrappers.Wildbook import Wildbook
import os


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root(wildbook: Wildbook = Depends(Wildbook)):
    wildbook_running = wildbook.is_running()

    connection = sqlite3.connect("sealcenter.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Seals LIMIT 1")
    row = cursor.fetchone()
    connection.close()

    return {
        "text": "Hello World",
        "wildbook": wildbook_running,
        "db": dict(row) if row else "No data found",
    }


# Upload seal without detection
@app.post("/seal/image")
async def upload_seal(
    image: UploadFile = File(...),
    name: str = Form(...),
    wildbook: Wildbook = Depends(Wildbook),
):
    if not image:  # Check for image
        return "No Image uploaded"

    # Save the file temporarily
    temp_image_path = "path_to_temp_storage"
    with open("path_to_temp_storage", "wb") as f:
        f.write(await image.read())

    # Upload image
    image_id = int(wildbook.upload_image(temp_image_path))

    # Clean up after upload
    os.remove(temp_image_path)

    # Get Image Size
    image_size = [0, 0] + list(wildbook.get_images_size(image_id)[0])

    # Detect the seal in the image
    aid_list = wildbook.create_annotations([image_id], [image_size], [name])

    return {"status": "success", "annotation_id": aid_list}


# Create Seal (MVP)
@app.post("/seal")
async def new_seal(
    image: UploadFile = File(...), wildbook: Wildbook = Depends(Wildbook)
):
    if not image:  # Check for image
        return "No Image uploaded"

    # Save the file temporarily
    temp_image_path = "path_to_temp_storage"
    with open("path_to_temp_storage", "wb") as f:
        f.write(await image.read())

    # Upload image
    image_id = wildbook.upload_image(temp_image_path)

    # Clean up after upload
    os.remove(temp_image_path)

    # Detect the seal in the image
    aid_list = wildbook.detect_seal([int(image_id)])

    # Match seal with seals in DB
    score = wildbook.seal_matching(aid_list[0])

    # Find aid and score for best match
    try:
        match_aid, match_score = next(iter(score.items()))
    except StopIteration:
        # Handle the case where there are no items
        match_aid, match_score = None, None

    # Get the uploaded image
    initial_image = wildbook.get_annotation_image(aid_list[0])

    # If there is a match, get the 'best match' image
    if match_aid:
        matched_image = wildbook.get_annotation_image(match_aid)
        matched_name = wildbook.get_annotation_name(match_aid)

        # Set the name of the seal
        wildbook.rename_annotations(
            aid_list, [matched_name]
        )  # Rename the uploaded image with the match name

        matched_image_base64 = matched_image.split(",", 1)[1]  # Remove the prefix
    else:
        # If there is no match, set a placeholder
        matched_image_base64 = None

    # Encode the initial as base64 for embedding in HTML
    initial_image_base64 = initial_image.split(",", 1)[1]  # Remove the prefix

    return {
        "initial_image": initial_image_base64,
        "matched_image": matched_image_base64,
        "match_aid": match_aid,
        "match_name": matched_name,
        "match_score": match_score,
        "initial_aid": aid_list[0],
    }


# Read Single Seal
@app.get("/seal/{seal_id}")
def read_seal(seal_id: str, wildbook: Wildbook = Depends(Wildbook)): ...


# List Seals
@app.get("/seals")
def list_seals(wildbook: Wildbook = Depends(Wildbook)):
    # Get the list of aids
    seal_aids = wildbook.list_annotations_id()
    seals_data = []

    # Get name and image for each Aid
    seal_images = {}
    for aid in seal_aids:
        seal_name = wildbook.get_annotation_name(aid)
        annotation_image = wildbook.get_annotation_image(aid)

        if seal_images.get(seal_name, None):
            seal_images[seal_name].append(annotation_image)
        else:
            seal_images[seal_name] = [annotation_image]

    # Return template with the data
    return seal_images


# Update Seals
@app.put("/seal/{seal_id}")
def update_seal(seal_id: str, wildbook: Wildbook = Depends(Wildbook)): ...


# Delete Seal
@app.delete("/seal/{seal_id}")
def remove_seal(seal_id: str, wildbook: Wildbook = Depends(Wildbook)): ...


# Create Sighting
@app.post("/sighting")
def add_sighting(wildbook: Wildbook = Depends(Wildbook)): ...


# Read Sighting
@app.get("/sighting/{sighting_id}")
def get_sighting(sighting_id: str, wildbook: Wildbook = Depends(Wildbook)): ...


# Update Sighting
@app.put("/sighting/{sighting_id}")
def edit_sighting(sighting_id: str, wildbook: Wildbook = Depends(Wildbook)): ...


# Delete Sighting
@app.delete("/sighting/{sighting_id}")
def remove_sighting(sighting_id: str, wildbook: Wildbook = Depends(Wildbook)): ...

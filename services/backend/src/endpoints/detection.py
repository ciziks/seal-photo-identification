from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from typing import List
import os
from src.wildbook import Wildbook
from src import constants

router = APIRouter()


@router.post("")
async def seal_matching(
    images: List[UploadFile] = File(...),
    wildbook: Wildbook = Depends(Wildbook),
):
    all_names_id = wildbook.list_names_id()

    names_list = wildbook.list_annotation_from_names(all_names_id)

    if not images or len(images) == 0:
        raise HTTPException(status_code=400, detail=constants.NO_IMAGE_MESSAGE)

    # Save the image temporarily
    image_id_list = []
    for image in images:
        temp_image_path = f"temp_{image.filename}"

        with open(temp_image_path, "wb") as f:
            f.write(await image.read())
        try:
            image_id_list.append(wildbook.upload_image(temp_image_path))
        finally:
            os.remove(temp_image_path)

    # Get Images Size
    image_size_list = [
        [0, 0] + list(image_size_list)
        for image_size_list in wildbook.get_images_size(image_id_list)
    ]

    # Create Annotations in WildBook
    annotation_id_list = wildbook.create_annotations(image_id_list, image_size_list)

    # Match batch of photos with seals in DB
    scores = wildbook.seal_matching(annotation_id_list, names_list)

    return scores

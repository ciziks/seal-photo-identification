from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src import constants
from src.wildbook import Wildbook
from src.crud.sighting import SightingCRUD
from src.schemas import Sighting, SightingCreate

router = APIRouter()


# CREATE SIGHTING REGISTER
@router.post("", response_model=Sighting)
def create_sighting(
    sighting: SightingCreate,
    crud_sighting: SightingCRUD = Depends(),
):
    existing_sighting = crud_sighting.get_sighting_from_date_location(
        sighting.Date, sighting.Location
    )

    if existing_sighting:
        new_sighting = existing_sighting
    else:
        new_sighting = crud_sighting.create_sighting(sighting=sighting)

    return new_sighting


# READ SIGHTING FROM SIGHTING ID
@router.get("/{sighting_id}")
def read_sighting(
    sighting_id: int,
    wildbook: Wildbook = Depends(Wildbook),
    crud_sighting: SightingCRUD = Depends(),
):
    db_sighting = crud_sighting.get_sighting_from_id(sighting_id=sighting_id)

    if not db_sighting:
        raise HTTPException(
            status_code=404, detail=constants.SIGHTING_NOT_FOUND_MESSAGE
        )

    sighting_images = []

    for encounter in db_sighting.encounters:
        annotation_image = wildbook.get_annotation_image(encounter.WildBookID)
        sighting_images.append(annotation_image)

    return {
        **db_sighting.__dict__,
        "images": sighting_images,
    }


# LIST SIGHTINGS WITH PAGINATION
@router.get("")
def list_sightings_with_pagination(
    skip: int = 0,
    limit: int = 10,
    wildbook: Wildbook = Depends(Wildbook),
    crud_sighting: SightingCRUD = Depends(),
):
    total_sightings, sightings = crud_sighting.list_sightings(
        skip=skip,
        limit=limit,
    )
    sightings_data = []

    for sighting in sightings:
        sighting_images = []
        for encounter in sighting.encounters:
            annotation_image = wildbook.get_annotation_image(encounter.WildBookID)
            sighting_images.append(annotation_image)

        sighting_dict = sighting.__dict__
        sighting_dict["images"] = sighting_images
        sightings_data.append(sighting_dict)

    return {
        "total": total_sightings,
        "limit": limit,
        "skip": skip,
        "data": sightings_data,
    }


# UPDATE SIGHTING INFORMATION
@router.put("/{sighting_id}", response_model=Sighting)
def update_sighting(
    sighting_id: int,
    sighting: SightingCreate,
    crud_sighting: SightingCRUD = Depends(),
):
    db_sighting = crud_sighting.get_sighting_from_id(sighting_id=sighting_id)

    if db_sighting is None:
        raise HTTPException(
            status_code=404, detail=constants.SIGHTING_NOT_FOUND_MESSAGE
        )

    return crud_sighting.update_sighting(db_sighting=db_sighting, sighting=sighting)


# DELETE SIGHTING AND RELATED ENCOUNTERS BY SIGHTING_ID
@router.delete("/{sighting_id}", response_model=Sighting)
def delete_sighting(sighting_id: int, crud_sighting: SightingCRUD = Depends()):
    db_sighting = crud_sighting.get_sighting_from_id(sighting_id=sighting_id)

    if db_sighting is None:
        raise HTTPException(
            status_code=404, detail=constants.SIGHTING_NOT_FOUND_MESSAGE
        )

    return crud_sighting.delete_sighting(db_sighting=db_sighting)


# DELETE SIGHTING AND RELATED ENCOUNTERS BY DATE AND LOCATION
@router.delete("/{location}/{date}", response_model=Sighting)
def delete_sighting_by_date_location(
    date: str, location: str, crud_sighting: SightingCRUD = Depends()
):
    try:
        parsed_date = datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail=constants.INVALID_DATE_MESSAGE)

    db_sighting = crud_sighting.find_sighting(parsed_date, location)

    if not db_sighting:
        raise HTTPException(
            status_code=404, detail=constants.SIGHTING_NOT_FOUND_MESSAGE
        )

    return crud_sighting.delete_sighting(db_sighting[0])


# SEARCH SIGHTING BY DATE AND LOCATION
@router.get("/search/")
def filter_sightings(
    date: Optional[str] = Query(None, description="Date in 'dd-mm-yyyy' format"),
    location: Optional[str] = Query(None, description="Location of the sighting"),
    wildbook: Wildbook = Depends(Wildbook),
    crud_sighting: SightingCRUD = Depends(),
):
    if date:
        try:
            parsed_date = datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=constants.INVALID_DATE_MESSAGE,
            )
    else:
        parsed_date = None

    sightings = crud_sighting.find_sighting(parsed_date, location)
    if not sightings:
        raise HTTPException(
            status_code=404, detail=constants.SIGHTING_NOT_FOUND_MESSAGE
        )

    sightings_data = []
    for sighting in sightings:
        sighting_images = []
        for encounter in sighting.encounters:
            annotation_image = wildbook.get_annotation_image(encounter.WildBookID)
            sighting_images.append(annotation_image)
        sighting_dict = sighting.__dict__
        sighting_dict["images"] = sighting_images
        sightings_data.append(sighting_dict)

    return sightings_data

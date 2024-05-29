from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.wildbook import Wildbook
from src.database import get_db
from src.constants import SEAL_NOT_FOUND_MESSAGE, SEAL_ALREADY_EXISTS_MESSAGE
from src import crud, schemas

router = APIRouter()


# CREATE NEW SEAL
@router.post("", response_model=schemas.Seal)
def create_seal(
    seal: schemas.SealCreate,
    db: Session = Depends(get_db),
):
    db_seal = crud.get_seal(db, seal_id=seal.ID)

    if db_seal:
        raise HTTPException(
            status_code=400, detail=SEAL_ALREADY_EXISTS_MESSAGE
        )

    return crud.create_seal(db=db, seal=seal)


# GET SEAL BY ID/NAME
@router.get("/{seal_id}")
def read_seal(
    seal_id: str,
    wildbook: Wildbook = Depends(Wildbook),
    db: Session = Depends(get_db),
):
    seal = crud.get_seal(db, seal_id=seal_id)

    if not seal:
        raise HTTPException(status_code=404, detail=SEAL_NOT_FOUND_MESSAGE)

    seal_encounters = []
    for encounter in seal.encounters:
        sighting = crud.get_sighting_from_id(db, sighting_id=encounter.SightingID)
        annotation_image = wildbook.get_annotation_image(encounter.WildBookID)
        encounter_data = {
            "WildBookID": encounter.WildBookID,
            "Date": sighting.Date if sighting else None,
            "Location": sighting.Location if sighting else None,
            "image": annotation_image
        }
        seal_encounters.append(encounter_data)
        

    return {**seal.__dict__, "encounters": seal_encounters}


# LIST SEAL WITH PAGINATION
@router.get("")
def list_seals_with_pagination(
    skip: int = 0,
    limit: int = 10,
    wildbook: Wildbook = Depends(Wildbook),
    db: Session = Depends(get_db),
):
    total_seals, seals = crud.list_seals(db, skip=skip, limit=limit)

    seals_with_encounter = {}
    for seal in seals:
        seals_with_encounter[seal.ID] = []

        if seal.encounters:
            annotation_image = wildbook.get_annotation_image(
                seal.encounters[-1].WildBookID
            )
            seals_with_encounter[seal.ID].append(annotation_image)

    return {
        "total": total_seals,
        "limit": limit,
        "skip": skip,
        "data": seals_with_encounter,
    }


# UPDATE SEAL INFORMATION
@router.put("/{seal_id}", response_model=schemas.Seal)
def update_seal(seal_id: str, seal: schemas.SealCreate, db: Session = Depends(get_db)):
    db_seal = crud.get_seal(db, seal_id=seal_id)

    if db_seal is None:
        raise HTTPException(status_code=404, detail=SEAL_NOT_FOUND_MESSAGE)

    return crud.update_seal(db=db, db_seal=db_seal, seal=seal)


# DELETE SEAL REGISTER AND RELATED ENCOUNTERS
@router.delete("/{seal_id}", response_model=schemas.Seal)
def delete_seal(seal_id: str, db: Session = Depends(get_db)):
    db_seal = crud.get_seal(db, seal_id=seal_id)

    if db_seal is None:
        raise HTTPException(status_code=404, detail=SEAL_NOT_FOUND_MESSAGE)

    return crud.delete_seal(db=db, seal=db_seal)

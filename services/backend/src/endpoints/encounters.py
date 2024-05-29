# app/api/endpoints/encounters.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, schemas, constants
from src.database import get_db

router = APIRouter()


@router.post("", response_model=schemas.Encounter)
def create_encounter(encounter: schemas.EncounterCreate, db: Session = Depends(get_db)):
    existing_sighting = crud.get_sighting_from_id(db, sighting_id=encounter.SightingID)

    if not existing_sighting:
        raise HTTPException(
            status_code=404, detail=constants.SIGHTING_NOT_FOUND_MESSAGE
        )

    existing_seal = crud.get_seal(db, seal_id=encounter.SealID)
    if not existing_seal:
        raise HTTPException(status_code=404, detail=constants.SEAL_NOT_FOUND_MESSAGE)

    return crud.create_encounter(db, encounter)

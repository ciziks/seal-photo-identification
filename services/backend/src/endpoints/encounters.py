from fastapi import APIRouter, Depends, HTTPException
from services.backend.src import constants
from services.backend.src.crud.encounter import EncounterDAO
from services.backend.src.crud.sighting import SightingDAO
from services.backend.src.crud.seal import SealDAO
from services.backend.src.schemas import EncounterSchema, EncounterCreate

router = APIRouter()


@router.post("", response_model=EncounterSchema)
def create_encounter(
    encounter: EncounterCreate,
    crud_encounter: EncounterDAO = Depends(),
    crud_sighting: SightingDAO = Depends(),
    crud_seal: SealDAO = Depends(),
):
    existing_sighting = crud_sighting.get_sighting_from_id(
        sighting_id=encounter.SightingID
    )

    if not existing_sighting:
        raise HTTPException(
            status_code=404, detail=constants.SIGHTING_NOT_FOUND_MESSAGE
        )

    existing_seal = crud_seal.get_seal(seal_id=encounter.SealID)
    if not existing_seal:
        raise HTTPException(status_code=404, detail=constants.SEAL_NOT_FOUND_MESSAGE)

    return crud_encounter.create_encounter(encounter)

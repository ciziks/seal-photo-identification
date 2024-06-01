from fastapi import Depends
from sqlalchemy.orm import Session

from services.backend.src.database import get_db
from services.backend.src.models import Encounter
from services.backend.src.schemas import EncounterCreate


class EncounterDAO:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # Method to create an Encounter in Database
    def create_encounter(self, encounter: EncounterCreate) -> Encounter:
        new_encounter = Encounter(**encounter.model_dump())
        self.db.add(new_encounter)
        self.db.commit()
        self.db.refresh(new_encounter)
        return new_encounter

    # Method to get an Encounter from Database
    def get_encounter(self, encounter_id: int) -> Encounter:
        return self.db.query(Encounter).filter(Encounter.WildBookID == encounter_id).first()

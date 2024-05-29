from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Encounter
from src.schemas import EncounterCreate

class EncounterCRUD:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_encounter(self, encounter: EncounterCreate):
        new_encounter = Encounter(**encounter.model_dump())
        self.db.add(new_encounter)
        self.db.commit()
        self.db.refresh(new_encounter)
        return new_encounter

    def get_encounter(self, encounter_id: int):
        return self.db.query(Encounter).filter(Encounter.id == encounter_id).first()


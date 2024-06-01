from typing import List, Tuple
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from services.backend.src.models import Seal
from services.backend.src.schemas import SealCreate
from services.backend.src.database import get_db


class SealDAO:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # Method to get a Seal from Database based on its SealID (same as Name)
    def get_seal(self, seal_id: str) -> Seal:
        return (
            self.db.query(Seal)
            .filter(Seal.ID == seal_id)
            .options(joinedload(Seal.encounters))
            .first()
        )

    # Method to list Seals from Database with pagination
    def list_seals(self, skip: int = 0, limit: int = 10) -> Tuple[int, List[Seal]]:
        seals_query = self.db.query(Seal).options(joinedload(Seal.encounters))
        total_seals = seals_query.count()
        selected_seals = seals_query.offset(skip).limit(limit).all()
        return total_seals, selected_seals

    # Method to create a new Sighting in DB
    def create_seal(self, seal: SealCreate) -> Seal:
        new_seal = Seal(**seal.model_dump())
        self.db.add(new_seal)
        self.db.commit()
        self.db.refresh(new_seal)
        return new_seal

    # Method to update Sighting's information in DB
    def update_seal(self, db_seal: Seal, seal: SealCreate) -> Seal:
        seal_data = seal.model_dump()
        for key, value in seal_data.items():
            setattr(db_seal, key, value)
        self.db.commit()
        self.db.refresh(db_seal)
        return db_seal

    # Method to remove a Sighting in DB
    def delete_seal(self, seal: Seal) -> Seal:
        self.db.delete(seal)
        self.db.commit()
        return seal

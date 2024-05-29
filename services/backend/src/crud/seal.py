from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from src.models import Seal
from src.schemas import SealCreate
from src.database import get_db


class SealCRUD:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_seal(self, seal_id: str):
        return (
            self.db.query(Seal)
            .filter(Seal.ID == seal_id)
            .options(joinedload(Seal.encounters))
            .first()
        )

    def list_seals(self, skip: int = 0, limit: int = 10):
        seals_query = self.db.query(Seal).options(joinedload(Seal.encounters))
        total_seals = seals_query.count()
        selected_seals = seals_query.offset(skip).limit(limit).all()
        return total_seals, selected_seals

    def create_seal(self, seal: SealCreate):
        new_seal = Seal(**seal.model_dump())
        self.db.add(new_seal)
        self.db.commit()
        self.db.refresh(new_seal)
        return new_seal

    def update_seal(self, db_seal: Seal, seal: SealCreate):
        seal_data = seal.model_dump()
        for key, value in seal_data.items():
            setattr(db_seal, key, value)
        self.db.commit()
        self.db.refresh(db_seal)
        return db_seal

    def delete_seal(self, seal: Seal):
        self.db.delete(seal)
        self.db.commit()
        return seal

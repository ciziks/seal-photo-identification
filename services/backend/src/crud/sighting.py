from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from src.models import Sighting
from src.schemas import SightingCreate
from src.database import get_db

class SightingCRUD:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_sighting_from_id(self, sighting_id: int):
        return (
            self.db.query(Sighting)
            .filter(Sighting.SightingID == sighting_id)
            .options(joinedload(Sighting.encounters))
            .first()
        )

    def get_sighting_from_date_location(self, date: datetime, location: str):
        return (
            self.db.query(Sighting)
            .filter(Sighting.Date == date, Sighting.Location == location)
            .options(joinedload(Sighting.encounters))
            .first()
        )

    def find_sighting(self, date: Optional[datetime] = None, location: Optional[str] = None):
        query = self.db.query(Sighting).options(joinedload(Sighting.encounters))
        if date:
            query = query.filter(func.date(Sighting.Date) == date.date())
        if location:
            query = query.filter(Sighting.Location == location)
        return query.all()

    def list_sightings(self, skip: int = 0, limit: int = 10):
        sighting_query = self.db.query(Sighting).options(joinedload(Sighting.encounters))
        total_sightings = sighting_query.count()
        selected_sightings = sighting_query.offset(skip).limit(limit).all()
        return total_sightings, selected_sightings

    def create_sighting(self, sighting: SightingCreate):
        db_sighting = Sighting(**sighting.model_dump())
        self.db.add(db_sighting)
        self.db.commit()
        self.db.refresh(db_sighting)
        return db_sighting

    def update_sighting(self, db_sighting: Sighting, sighting: SightingCreate):
        sighting_data = sighting.model_dump()
        for key, value in sighting_data.items():
            setattr(db_sighting, key, value)
        self.db.commit()
        self.db.refresh(db_sighting)
        return db_sighting

    def delete_sighting(self, db_sighting: Sighting):
        self.db.delete(db_sighting)
        self.db.commit()
        return db_sighting

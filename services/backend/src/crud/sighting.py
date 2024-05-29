from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from src.models import Sighting
from src.schemas import SightingCreate
from src.database import get_db


class SightingDAO:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # Method to get a Sighting from Database based on its SightingID
    def get_sighting_from_id(self, sighting_id: int) -> Sighting:
        return (
            self.db.query(Sighting)
            .filter(Sighting.SightingID == sighting_id)
            .options(joinedload(Sighting.encounters))
            .first()
        )

    # Method to find a Sighting from Database based on its Date and Location
    def find_sighting(
        self, date: Optional[datetime] = None, location: Optional[str] = None
    ) -> Sighting:
        query = self.db.query(Sighting).options(joinedload(Sighting.encounters))
        if date:
            query = query.filter(func.date(Sighting.Date) == date.date())
        if location:
            query = query.filter(Sighting.Location == location)
        return query.all()

    # Method to list Sightings from Database with pagination
    def list_sightings(
        self, skip: int = 0, limit: int = 10
    ) -> Tuple[int, List[Sighting]]:
        sighting_query = self.db.query(Sighting).options(
            joinedload(Sighting.encounters)
        )
        total_sightings = sighting_query.count()
        selected_sightings = sighting_query.offset(skip).limit(limit).all()
        return total_sightings, selected_sightings

    # Method to create a new Sighting in DB
    def create_sighting(self, sighting: SightingCreate) -> Sighting:
        db_sighting = Sighting(**sighting.model_dump())
        self.db.add(db_sighting)
        self.db.commit()
        self.db.refresh(db_sighting)
        return db_sighting

    # Method to update Sighting's information in DB
    def update_sighting(
        self, db_sighting: Sighting, sighting: SightingCreate
    ) -> Sighting:
        sighting_data = sighting.model_dump()
        for key, value in sighting_data.items():
            setattr(db_sighting, key, value)
        self.db.commit()
        self.db.refresh(db_sighting)
        return db_sighting

    # Method to remove a Sighting in DB
    def delete_sighting(self, db_sighting: Sighting) -> Sighting:
        self.db.delete(db_sighting)
        self.db.commit()
        return db_sighting

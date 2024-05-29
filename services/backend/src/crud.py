from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from .models import Encounter, Seal, Sighting
from .schemas import EncounterCreate, SealCreate, SightingCreate


# CRUD - SEALS
def get_seal(
    db: Session,
    seal_id: str,
):
    return (
        db.query(Seal)
        .filter(Seal.ID == seal_id)
        .options(joinedload(Seal.encounters))
        .first()
    )


def list_seals(
    db: Session,
    skip: int = 0,
    limit: int = 10,
):
    seals_query = db.query(Seal).options(joinedload(Seal.encounters))
    total_seals = seals_query.count()
    selected_seals = seals_query.offset(skip).limit(limit).all()
    return total_seals, selected_seals


def create_seal(
    db: Session,
    seal: SealCreate,
):
    seal = Seal(**seal.model_dump())
    db.add(seal)
    db.commit()
    db.refresh(seal)
    return seal


def update_seal(
    db: Session,
    db_seal: Seal,
    seal: SealCreate,
):
    seal_data = seal.model_dump()
    for key, value in seal_data.items():
        setattr(db_seal, key, value)

    db.commit()
    db.refresh(db_seal)
    return db_seal


def delete_seal(db: Session, seal: Seal):
    db.delete(seal)
    db.commit()
    return seal


# CRUD - SIGHTINGS
def get_sighting_from_id(
    db: Session,
    sighting_id: int,
):
    return (
        db.query(Sighting)
        .filter(Sighting.SightingID == sighting_id)
        .options(joinedload(Sighting.encounters))
        .first()
    )


def get_sighting_from_date_location(
    db: Session,
    date: datetime,
    location: str,
):
    return (
        db.query(Sighting)
        .filter(Sighting.Date == date, Sighting.Location == location)
        .options(joinedload(Sighting.encounters))
        .first()
    )


def find_sighting(
    db: Session,
    date: Optional[datetime] = None,
    location: Optional[str] = None,
):
    query = db.query(Sighting).options(joinedload(Sighting.encounters))
    if date:
        query = query.filter(func.date(Sighting.Date) == date.date())
    if location:
        query = query.filter(Sighting.Location == location)

    return query.all()


def list_sightings(
    db: Session,
    skip: int = 0,
    limit: int = 10,
):
    sighting_query = db.query(Sighting).options(joinedload(Sighting.encounters))
    total_sightings = sighting_query.count()
    selected_sightings = sighting_query.offset(skip).limit(limit).all()

    return total_sightings, selected_sightings


def create_sighting(
    db: Session,
    sighting: SightingCreate,
):
    db_sighting = Sighting(**sighting.model_dump())
    db.add(db_sighting)
    db.commit()
    db.refresh(db_sighting)
    return db_sighting


def update_sighting(db: Session, db_sighting: Sighting, sighting: SightingCreate):
    sighting_data = sighting.model_dump()
    for key, value in sighting_data.items():
        setattr(db_sighting, key, value)
    db.commit()
    db.refresh(db_sighting)
    return db_sighting


def delete_sighting(db: Session, db_sighting: Sighting):
    db.delete(db_sighting)
    db.commit()
    return db_sighting


# CRUD - Encounters
def create_encounter(db: Session, encounter: EncounterCreate):
    new_encounter = Encounter(**encounter.model_dump())
    db.add(new_encounter)
    db.commit()
    db.refresh(new_encounter)
    return new_encounter

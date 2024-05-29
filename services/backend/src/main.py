# app/main.py
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError, DatabaseError
from sqlalchemy.orm import Session
from src.database import engine, Base, get_db
from .exceptions import (
    sqlalchemy_data_error_handler,
    sqlalchemy_database_error_handler,
    sqlalchemy_exception_handler,
    sqlalchemy_integrity_error_handler,
)
from .endpoints import seals, sightings, encounters, detection, export
from .wildbook import Wildbook

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(seals.router, prefix="/seals", tags=["seals"])
app.include_router(sightings.router, prefix="/sightings", tags=["sightings"])
app.include_router(encounters.router, prefix="/encounters", tags=["encounters"])
app.include_router(detection.router, prefix="/detect", tags=["detect"])
app.include_router(export.router, prefix="/export", tags=["export"])


@app.get("/")
def root(wildbook: Wildbook = Depends(Wildbook), db: Session = Depends(get_db)):
    wildbook_running = wildbook.is_running()

    return {
        "message": "Hello Seals!",
        "wildbook": wildbook_running,
    }


app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(IntegrityError, sqlalchemy_integrity_error_handler)
app.add_exception_handler(DataError, sqlalchemy_data_error_handler)
app.add_exception_handler(DatabaseError, sqlalchemy_database_error_handler)

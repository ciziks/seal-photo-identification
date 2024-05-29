# app/api/endpoints/export.py
import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Sighting, Seal, Encounter

router = APIRouter()


@router.get("")
def export_data(db: Session = Depends(get_db)):
    # Query all data from the tables
    sightings = pd.read_sql(db.query(Sighting).statement, db.bind)
    seals = pd.read_sql(db.query(Seal).statement, db.bind)
    encounters = pd.read_sql(db.query(Encounter).statement, db.bind)

    # Merge the data into a single DataFrame
    merged_data = sightings.merge(
        encounters,
        how="left",
        left_on="SightingID",
        right_on="SightingID",
        validate="one_to_many",
    )
    merged_data = merged_data.merge(
        seals, how="left", left_on="SealID", right_on="ID", validate="many_to_one"
    )

    # Drop redundant columns
    merged_data = merged_data.drop(columns=["ID"])

    # Create a Pandas Excel writer using openpyxl as the engine
    output_path = "sealcenter_data.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        merged_data.to_excel(writer, sheet_name="SealCenter", index=False)

    # Return the file as a response
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=output_path,
    )

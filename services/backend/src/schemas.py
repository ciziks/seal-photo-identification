from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime


class EncounterSchema(BaseModel):
    SightingID: int
    SealID: str
    WildBookID: int

    class Config:
        orm_mode = True


class EncounterCreate(EncounterSchema):
    ...
    
class SealSchema(BaseModel):
    ID: str
    age: str
    description: Optional[str] = None
    gender: Optional[str] = None
    isPregnant: Optional[str] = None


class SealCreate(SealSchema):
    pass


class Seal(SealSchema):
    encounters: List[EncounterSchema] = []

    class Config:
        orm_mode = True


class SightingSchema(BaseModel):
    Date: datetime
    Location: str


class SightingCreate(SightingSchema):
    @validator("Date", pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y")
        return value


class Sighting(SightingSchema):
    SightingID: int
    encounters: List[EncounterSchema] = []
    images: List[str] = []

    class Config:
        orm_mode = True

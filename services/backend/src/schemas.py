from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime


class SealBase(BaseModel):
    ID: str
    age: str
    comments: Optional[str] = None
    gender: Optional[str] = None
    isPregnant: Optional[str] = None


class SealCreate(SealBase):
    pass


class EncounterSchema(BaseModel):
    SightingID: int
    SealID: str
    WildBookID: int

    class Config:
        orm_mode = True


class EncounterCreate(BaseModel):
    SightingID: int
    SealID: str
    WildBookID: int


class Encounter(BaseModel):
    SightingID: int
    SealID: str
    WildBookID: int

    class Config:
        orm_mode = True


class Seal(SealBase):
    encounters: List[EncounterSchema] = []

    class Config:
        orm_mode = True


class SightingBase(BaseModel):
    Date: datetime
    Location: str


class SightingCreate(SightingBase):
    @validator("Date", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(value, "%d/%m/%Y")


class Sighting(SightingBase):
    SightingID: int
    encounters: List[EncounterSchema] = []
    images: List[str] = []

    class Config:
        orm_mode = True

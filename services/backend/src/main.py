from typing import Union
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .wrappers.Wildbook import Wildbook


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return "Hello World"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Create Seal
@app.get("/seal")
def new_seal(wildbook=Depends(Wildbook)): ...


# Read Single Seal
@app.get("/seal/{seal_id}")
def read_seal(seal_id: str, wildbook=Depends(Wildbook)): ...


# List Seals
@app.get("/seals")
def list_seals(wildbook=Depends(Wildbook)): ...


# Update Seals
@app.put("/seal/{seal_id}")
def update_seal(seal_id: str, wildbook=Depends(Wildbook)): ...


# Delete Seal
@app.delete("/seal/{seal_id}")
def remove_seal(seal_id: str, wildbook=Depends(Wildbook)): ...


# Create Sighting
@app.post("/sighting")
def add_sighting(wildbook=Depends(Wildbook)): ...


# Read Sighting
@app.get("/sighting/{sighting_id}")
def get_sighting(sighting_id: str, wildbook=Depends(Wildbook)): ...


# Update Sighting
@app.put("/sighting/{sighting_id}")
def edit_sighting(sighting_id: str, wildbook=Depends(Wildbook)): ...


# Delete Sighting
@app.delete("/sighting/{sighting_id}")
def remove_sighting(sighting_id: str, wildbook=Depends(Wildbook)): ...

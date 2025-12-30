from fastapi import APIRouter, HTTPException, status, UploadFile, File
from typing import List
from app.models.db_models import Generos
from app.pb_clients.generos import (
    db_get_genero,
    db_get_all_generos,
    db_create_genero,
    db_update_genero,
    db_delete_genero
)

router = APIRouter(
    prefix="/generos",
    tags=["Generos"],
)

# Get all generos
@router.get("/", response_model=List[Generos], summary="Get all Generos")
@router.get("", response_model=List[Generos], summary="Get all Generos")
def api_get_all_generos():
    try:
        return db_get_all_generos()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Get genero by ID
@router.get("/{pk_id_genero}", response_model=Generos, summary="Get a Genero by ID")
def api_get_genero(pk_id_genero: int):
    try:
        return db_get_genero(pk_id_genero)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Create a new genero
@router.post("/create/", response_model=Generos, summary="Create a new Genero")
def api_create_genero(genero: Generos):
    try:
        return db_create_genero(genero)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Update an existing genero
@router.patch("/update/", response_model=Generos, summary="Update a Genero")
def api_update_genero(genero: Generos):
    try:
        return db_update_genero(genero)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Delete a genero by ID
@router.delete("/delete/{pk_id_genero}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Genero by ID")
def api_delete_genero(pk_id_genero: int):
    try:
        db_delete_genero(pk_id_genero)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

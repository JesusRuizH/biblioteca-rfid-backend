from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.pb_clients.departamento import (
    db_get_departamento,
    db_create_departamento,
    db_update_departamento,
    db_delete_departamento, db_get_all_dptos,
)
from app.models.db_models import Departamento

router = APIRouter(
    prefix="/departamento",
    tags=["Departamentos"],  # Grouped under "Departamentos" in Swagger UI
)

@router.get("/", response_model=List[Departamento], summary="Get all Depas")
@router.get("", response_model=List[Departamento], summary="Get all Depas")
def api_db_get_all_dptos():
    try:
        return db_get_all_dptos()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/get/{pk_id_departamento}", response_model=Departamento, summary="Get a Departamento by pk_id_departamento")
def api_get_departamento(pk_id_departamento: int):
    """
    Fetch a single Departamento by its primary key ID.

    - **pk_id_departamento**: The ID of the department to fetch.
    """
    try:
        return db_get_departamento(pk_id_departamento)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/create/", response_model=Departamento, summary="Create a new Departamento")
def api_create_departamento(departamento: Departamento):
    """
    Create a new Departamento.
    """
    try:
        return db_create_departamento(departamento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update/", response_model=Departamento, summary="Update a Departamento")
def api_update_departamento(departamento: Departamento):
    """
    Update an existing Departamento.
    """
    try:
        return db_update_departamento(departamento)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{pk_id_departamento}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Departamento")
def api_delete_departamento(pk_id_departamento: int):
    """
    Delete a Departamento by its primary key ID.

    - **pk_id_departamento**: The ID of the department to delete.
    """
    try:
        db_delete_departamento(pk_id_departamento)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

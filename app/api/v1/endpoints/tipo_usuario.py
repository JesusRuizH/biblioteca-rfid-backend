from typing import List

from fastapi import APIRouter, HTTPException, status
from app.pb_clients.tipo_usuario import (
    db_get_tipo_usuario,
    db_create_tipo_usuario,
    db_update_tipo_usuario,
    db_delete_tipo_usuario,
    db_get_all_tipo_usuario
)
from app.models.db_models import TipoUsuario

router = APIRouter(
    prefix="/tipo_usuario",
    tags=["Tipo Usuario"],  # Grouped under "Tipo Usuario" in Swagger UI
)

@router.get("/all", response_model=List[TipoUsuario], summary="Get all TipoUsuario")
@router.get("/all/", response_model=List[TipoUsuario], summary="Get all TipoUsuario")
def api_db_get_all_tipo_usuario():
    """
    Fetch a single TipoUsuario by its ID.

    - **pk_id_tipo_usuario**: The ID of the user type to fetch.
    """
    try:
        return db_get_all_tipo_usuario()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
@router.get("/{pk_id_tipo_usuario}", response_model=TipoUsuario, summary="Get a TipoUsuario by ID")
def api_get_tipo_usuario(pk_id_tipo_usuario: int):
    """
    Fetch a single TipoUsuario by its ID.

    - **pk_id_tipo_usuario**: The ID of the user type to fetch.
    """
    try:
        return db_get_tipo_usuario(pk_id_tipo_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create/", response_model=TipoUsuario, summary="Create a new TipoUsuario")
def api_create_tipo_usuario(tipo_usuario: TipoUsuario):
    """
    Create a new TipoUsuario.
    """
    try:
        return db_create_tipo_usuario(tipo_usuario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update/", response_model=TipoUsuario, summary="Update a TipoUsuario")
def api_update_tipo_usuario(tipo_usuario: TipoUsuario):
    """
    Update an existing TipoUsuario.
    """
    try:
        return db_update_tipo_usuario(tipo_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{pk_id_tipo_usuario}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a TipoUsuario by ID")
def api_delete_tipo_usuario(pk_id_tipo_usuario: int):
    """
    Delete a TipoUsuario by its ID.

    - **pk_id_tipo_usuario**: The ID of the user type to delete.
    """
    try:
        db_delete_tipo_usuario(pk_id_tipo_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

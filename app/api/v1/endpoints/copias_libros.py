from typing import Dict, List

from fastapi import APIRouter, HTTPException, status
from app.pb_clients.copias_libros import (
    db_get_copia_libro,
    db_create_copia_libro,
    db_update_copia_libro,
    db_delete_copia_libro,
    db_get_copia_libro_rfid,
    db_update_stat_copia_libro_prestado, db_update_stat_copia_libro_devuelto, db_get_ultimo_id_copia, db_get_all_copies
)
from app.models.db_models import CopiaLibro

router = APIRouter(
    prefix="/copia_libro",
    tags=["Copias"],  # Grouped under "Copias" in Swagger UI
)

@router.get("/get_all_copies", response_model=List, summary="Get all books")
@router.get("/get_all_copies/", response_model=List, summary="Get all books")
def api_db_get_all_copies():
    """
    Fetch a single préstamo (loan) by its ID.

    - **prestamo_id**: The ID of the loan to fetch.
    """
    try:
        return db_get_all_copies()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/ultimo_id_copia", response_model=int, summary="Get last registered pk_id_usuario from users")
@router.get("/ultimo_id_copia/", response_model=int, summary="Get last registered pk_id_usuario from users")
def api_db_get_ultimo_id_copia():
    """
    Fetch a single usuario by its ID.

    - **pk_id_usuario**: The ID of the user to fetch.
    """
    try:
        return db_get_ultimo_id_copia()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{pk_id_copia}", response_model=CopiaLibro, summary="Get a CopiaLibro by pk_id_copia")
def api_get_copia_libro(pk_id_copia: int):
    """
    Fetch a single CopiaLibro by its primary key ID.

    - **pk_id_copia**: The ID of the book copy to fetch.
    """
    try:
        return db_get_copia_libro(pk_id_copia)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/rfid/{rfid}", response_model=Dict, summary="Get a CopiaLibro by pk_id_copia")
def api_get_copia_libro(rfid: str):
    """
    Fetch a single CopiaLibro by its primary key ID.

    - **pk_id_copia**: The ID of the book copy to fetch.
    """
    try:
        return db_get_copia_libro_rfid(rfid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/stat_copia_libro_prestado/{pk_id_copia}", response_model=bool, summary="Update status to false for loaned book")
def api_db_update_stat_copia_libro_prestado(pk_id_copia: int):
    """
    Fetch a single CopiaLibro by its primary key ID.

    - **pk_id_copia**: The ID of the book copy to fetch.
    """
    try:
        if db_update_stat_copia_libro_prestado(pk_id_copia):
            return True
        return False
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/stat_copia_libro_devuelto/{pk_id_copia}", response_model=bool, summary="Update status to false for loaned book")
def api_db_update_stat_copia_libro_devuelto(pk_id_copia: int):
    """
    Fetch a single CopiaLibro by its primary key ID.

    - **pk_id_copia**: The ID of the book copy to fetch.
    """
    try:
        if db_update_stat_copia_libro_devuelto(pk_id_copia):
            return True
        return False
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/create", response_model=CopiaLibro, summary="Create a new CopiaLibro")
@router.post("/create/", response_model=CopiaLibro, summary="Create a new CopiaLibro")
def api_create_copia_libro(copia_libro: CopiaLibro):
    """
    Create a new CopiaLibro (book copy).
    """
    try:
        return db_create_copia_libro(copia_libro)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update/", response_model=CopiaLibro, summary="Update a CopiaLibro")
@router.patch("/update", response_model=CopiaLibro, summary="Update a CopiaLibro")
def api_update_copia_libro(copia_libro: CopiaLibro):
    """
    Update an existing CopiaLibro.
    """
    try:
        return db_update_copia_libro(copia_libro)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{pk_id_copia}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a CopiaLibro by ID")
def api_delete_copia_libro(pk_id_copia: int):
    """
    Delete a CopiaLibro by its internal PocketBase ID.

    - **id**: The PocketBase record ID of the book copy to delete.
    """
    try:
        db_delete_copia_libro(pk_id_copia)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

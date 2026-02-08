from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Query
from app.pb_clients.libros import db_get_libro, db_create_libro, db_delete_libro, db_update_libro, db_get_all_libros, \
    db_get_all, db_get_last_id_libro, db_get_libros_paginados, db_get_libros_lista_paginados
from app.models.db_models import Libro

router = APIRouter(
    prefix="/libro",
    tags=["Libros"],  # Grouped under "Prestamos" in Swagger UI
)

@router.get("/get_all", response_model=[], summary="Get all books")
@router.get("/get_all/", response_model=[], summary="Get all books")
def api_get_all():
    """
    Fetch a single préstamo (loan) by its ID.

    - **prestamo_id**: The ID of the loan to fetch.
    """
    try:
        return db_get_all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/get_list_libros", response_model=[], summary="Get a book by pk_id_libro")
def get_list_libros(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    q: Optional[str] = Query(None),
):
    """
    Obtenemos los usuarios por páginación
    """
    try:
        return db_get_libros_lista_paginados(limit, offset, q)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/ultimo_libro_id", response_model=int, summary="Get last registered book")
@router.get("/ultimo_libro_id/", response_model=int, summary="Get last registered book")
def api_db_get_estadisticas_admin_panel_a():
    """
    Fetch a single usuario by its ID.

    - **pk_id_usuario**: The ID of the user to fetch.
    """
    try:
        return db_get_last_id_libro()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/get", response_model=[], summary="Get a book by pk_id_libro")
@router.get("/get/", response_model=[], summary="Get a book by pk_id_libro")
def get_libros(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    """
    Obtenemos los libros por páginación
    """
    try:
        return db_get_libros_paginados(limit, offset)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/get/{pk_id_libro}", response_model=Libro, summary="Get a book by pk_id_libro")
def api_get_prestamo(pk_id_libro: int):
    """
    Fetch a single préstamo (loan) by its ID.

    - **prestamo_id**: The ID of the loan to fetch.
    """
    try:
        return db_get_libro(pk_id_libro)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/get/ultimos/{cantidad}", response_model=[], summary="Get a book by pk_id_libro")
def api_get_all_libros(cantidad: int):
    """
    Fetch a single préstamo (loan) by its ID.

    - **prestamo_id**: The ID of the loan to fetch.
    """
    try:
        return db_get_all_libros(cantidad)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/create/", response_model=Libro)
@router.post("/create", response_model=Libro)
def api_create_prestamo(libro: Libro):
    # Aquí guardarías a la base de datos o llamas a otra función
    try:
        return db_create_libro(libro)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{pk_id_libro}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a book by pk_id_libro")
def api_delete_libro(pk_id_libro: int):
    """
    Delete a book by its primary key ID.

    - **pk_id_libro**: The ID of the book to delete.
    """
    try:
        db_delete_libro(pk_id_libro)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/update/", response_model=Libro, summary="Update the book based on the full book")
@router.patch("/update", response_model=Libro, summary="Update the book based on the full book")
def api_update_prestamo(libro: Libro):
    """
    Fetch a single préstamo (loan) by its ID.

    - **prestamo_id**: The ID of the loan to fetch.
    """
    try:
        return db_update_libro(libro)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
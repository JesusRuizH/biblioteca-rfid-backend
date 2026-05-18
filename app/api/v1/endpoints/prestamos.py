from typing import List, Optional, Dict

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel

from app.pb_clients.prestamos import (
    db_get_prestamo,
    db_create_prestamo,
    db_update_prestamo,
    db_delete_prestamo,
    db_get_top_libros,
    db_get_mis_prestamos_pendientes,
    db_get_historial_prestamos,
    db_get_generos_leidos,
    db_get_prestamos_por_mes,
    db_get_prestamos_por_mes_admin,
    db_get_historial_prestamos_admin,
    db_get_generos_leidos_admin,
    db_get_total_prestamos,
    db_get_total_mis_prestamos,
    db_get_last_id_prestamos,
    get_libros_cache,
    db_get_mis_recomendaciones,
    db_get_historial_paginado,
    db_get_generos_leidos_usuario,
    db_get_historial_por_fechas
)
from app.models.db_models import Prestamo

router = APIRouter(
    prefix="/prestamo",
    tags=["Prestamos"],  # Grouped under "Prestamos" in Swagger UI
)


class PrestamoMes(BaseModel):
    mes: str
    prestamos: int

@router.get("/get_historial_paginado/", response_model=[], summary="Get historial páginado")
@router.get("/get_historial_paginado", response_model=[], summary="Get historial páginado")
def get_list_libros(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    """
    Obtenemos los usuarios por páginación
    """
    try:
        return db_get_historial_paginado(offset, limit)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/get_historial_fechas/", response_model=[], summary="Get historial páginado")   
@router.get("/get_historial_fechas", response_model=[], summary="Get historial páginado")
def get_list_libros(
    start_date: str,
    end_date: str,
):
    """
    Obtenemos los usuarios por páginación
    """
    try:
        return db_get_historial_por_fechas(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/total_mis_prestamos/{fk_id_usuario}", response_model=Dict, summary="Get a count of full loans")
def api_db_get_total_mis_prestamos(fk_id_usuario :str):
    """
    Fetch a single préstamo (loan) by its ID.

    - **top**: Recupera el top de libros indicado por el usuario.
    """
    try:
        return db_get_total_mis_prestamos(fk_id_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/prestamos_totales/", response_model=int, summary="Get a count of full loans")
@router.get("/prestamos_totales", response_model=int, summary="Get a count of full loans")
def api_db_get_total_prestamos():
    """
    Fetch a single préstamo (loan) by its ID.

    - **top**: Recupera el top de libros indicado por el usuario.
    """
    try:
        return db_get_total_prestamos()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/mis_prestamos_por_mes_admin", response_model=List[PrestamoMes])
@router.get("/mis_prestamos_por_mes_admin/", response_model=List[PrestamoMes])
def api_db_get_prestamos_por_mes_admin():
    """
    Fetch loans aggregated by month.
    """
    try:
        return db_get_prestamos_por_mes_admin()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/mis_generos_leidos_admin", response_model=[], summary="get gnre based on pk_id_usuario ")
@router.get("/mis_generos_leidos_admin/", response_model=[], summary="get gnre based on pk_id_usuario ")
def api_db_get_generos_leidos_admin():
    """
    Fetch a single préstamo (loan) by its ID.

    - **pk_id_usuario**: Recupera prestamos pendientes por usuario en base a su ID
    """
    try:
        return db_get_generos_leidos_admin()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/generos_leidos_usuario/{fk_id_usuario}", response_model=[], summary="get gnre based on pk_id_usuario ")
def api_db_get_generos_leidos_usuario(fk_id_usuario: str):
    """
    Fetch a single préstamo (loan) by its ID.

    - **pk_id_usuario**: Recupera prestamos pendientes por usuario en base a su ID
    """
    try:
        return db_get_generos_leidos_usuario(fk_id_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/historial_prestamos_admin/{cantidad}", response_model=[], summary="get last 5 loans")
def api_db_get_historial_prestamos_admin(cantidad : int):
    """
    Fetch a single préstamo (loan) by its ID.

    - **pk_id_usuario**: Recupera prestamos pendientes por usuario en base a su ID
    """
    try:
        return db_get_historial_prestamos_admin(cantidad)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/ultimo_prestamo_id/", response_model=[], summary="get last prestamo id")
@router.get("/ultimo_prestamo_id", response_model=[], summary="get last prestamo id")
def api_db_get_last_id_prestamos():
    """
    Fetch a single préstamo (loan) by its ID.

    - **pk_id_usuario**: Recupera prestamos pendientes por usuario en base a su ID
    """
    try:
        return db_get_last_id_prestamos()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{pk_id_prestamo}", response_model=Prestamo, summary="Get a Prestamo by pk_id_prestamo")
def api_get_prestamo(pk_id_prestamo: int):
    """
    Fetch a single préstamo (loan) by its ID.

    - **pk_id_prestamo**: The ID of the loan to fetch.
    """
    try:
        return db_get_prestamo(pk_id_prestamo)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/populares/{top}", response_model=[], summary="Get a Prestamo by pk_id_prestamo")
def api_db_get_top_libros(top: int):
    """
    Fetch a single préstamo (loan) by its ID.

    - **top**: Recupera el top de libros indicado por el usuario.
    """
    try:
        return get_libros_cache()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/mis_prestamos/{pk_id_usuario}", response_model=[], summary="get loans based on pk_id_usuario ")
def api_db_get_mis_prestamos_pendientes(pk_id_usuario: int):
    """
    Fetch a single préstamo (loan) by its ID.

    - **pk_id_usuario**: Recupera prestamos pendientes por usuario en base a su ID
    """
    try:
        return db_get_mis_prestamos_pendientes(pk_id_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/mis_prestamos_por_mes/{fk_id_usuario}", response_model=[], summary="get loans based on fk_id_usuario ")
def api_db_get_prestamos_por_mes(fk_id_usuario: str):
    """
    Fetch a single préstamo (loan) by its ID.

    - **fk_id_usuario**: Recupera prestamos pendientes por usuario en base a su ID
    """
    try:
        return db_get_prestamos_por_mes(fk_id_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get("/historial_prestamos/{fk_id_usuario}", summary="Obtener historial de préstamos paginado")
def api_db_get_historial_prestamos(
    fk_id_usuario: str, 
    page: int = Query(1, ge=1),                  # Default page 1, minimum 1
    limit: int = Query(10, gt=0, le=100)         # Default 10, min 1, max 100
):
    """
    Recupera los préstamos de un usuario de forma paginada.
    
    - **fk_id_usuario**: ID único del usuario en PocketBase.
    - **page**: El número de página actual.
    - **limit**: Cantidad de registros por página.
    """
    try:
        res = db_get_historial_prestamos(fk_id_usuario, page, limit)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    
@router.get("/mis_recomendaciones/{pk_id_usuario}", response_model=[], summary="get loans based on pk_id_usuario ")
def api_db_get_mis_recomendaciones(pk_id_usuario: int):
    """
    Fetch a single préstamo (loan) by its ID.

    - **pk_id_usuario**: Recupera una lista de recomendación basada en Machine Learning y arboles de decision
    """
    try:
        return db_get_mis_recomendaciones(pk_id_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/mis_generos_leidos/{pk_id_usuario}", response_model=[], summary="get gnre based on pk_id_usuario ")
def api_db_get_generos_leidos(pk_id_usuario: int):
    """
    Fetch a single préstamo (loan) by its ID.

    - **pk_id_usuario**: Recupera prestamos pendientes por usuario en base a su ID
    """
    try:
        return db_get_generos_leidos(pk_id_usuario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/create", response_model=Prestamo, summary="Create a new Prestamo")
@router.post("/create/", response_model=Prestamo, summary="Create a new Prestamo")
def api_create_prestamo(prestamo: Prestamo):
    """
    Create a new préstamo (loan).
    """
    try:
        return db_create_prestamo(prestamo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update/", response_model=Prestamo, summary="Update a Prestamo")
def api_update_prestamo(prestamo: Prestamo):
    """
    Update an existing préstamo (loan).
    """
    try:
        return db_update_prestamo(prestamo)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{pk_id_prestamo}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Prestamo by ID")
def api_delete_prestamo(pk_id_prestamo: int):
    """
    Delete a préstamo (loan) by its ID.

    - **pk_id_prestamo**: The ID of the loan to delete.
    """
    try:
        db_delete_prestamo(pk_id_prestamo)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

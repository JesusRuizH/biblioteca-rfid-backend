from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Query
from app.pb_clients.estadisticas import db_get_statistics

router = APIRouter(
    prefix="/estadisticas",
    tags=["Estadisticas"],
)

@router.get("/get_statistics", response_model={}, summary="Get all statistics at once")
@router.get("/get_statistics/", response_model={}, summary="Get all statistics at once")
def api_get_statistics():
    """
    Get all statistics

    """
    try:
        return db_get_statistics()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
   
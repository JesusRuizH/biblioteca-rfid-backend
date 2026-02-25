from typing import List

from app.services.recomendaciones_service import (
    db_get_recomendaciones,
)


from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/recomendaciones-usuario",
    tags=["Recomendaciones"],  
)

@router.get("/get_recomendaciones", response_model=List, summary="Get recomendaciónes de usuarios")
def api_get_all(id: str):
    """
    Se obtiene id del usuario para buscar sus recomendaciónes
    """
    try:
        return db_get_recomendaciones(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
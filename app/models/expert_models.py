from pydantic import BaseModel
from typing import Optional, List, Any, Dict


# ── Sesión ────────────────────────────────────────────────────────────────────

class SesionInicio(BaseModel):
    sesion_id: str
    pregunta: str
    clave: str
    opciones: List[str]
    progreso: int
    total: int


class RespuestaUsuario(BaseModel):
    sesion_id: str
    clave: str
    valor: str


# ── Resultado final ───────────────────────────────────────────────────────────

class LibroConfianza(BaseModel):
    """Un libro del top 3 con su porcentaje de confianza."""
    pk_id_libro: int
    confianza: float        # porcentaje, ej: 85.5
    libro: Optional[Dict[str, Any]] = None  # datos completos del libro


# ── Respuesta unificada por turno ─────────────────────────────────────────────

class TurnoRecomendador(BaseModel):
    """
    finalizado=False → hay más preguntas
    finalizado=True  → devuelve top3 + explicación
    """
    sesion_id: str
    finalizado: bool

    # Campos de pregunta (cuando finalizado=False)
    pregunta: Optional[str] = None
    clave: Optional[str] = None
    opciones: Optional[List[str]] = None
    progreso: Optional[int] = None
    total: Optional[int] = None

    # Campos de resultado (cuando finalizado=True)
    top3: Optional[List[LibroConfianza]] = None
    explicacion: Optional[str] = None
    modo: Optional[str] = None          # "exacto" o "sugerencias"
    entrenado_con: Optional[int] = None # cantidad de libros usados para entrenar
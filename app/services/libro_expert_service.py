"""
libro_expert_service.py
-----------------------
Singleton del LibroExpertSystem y helpers para obtener libros completos.
"""

from typing import Dict, Any, Optional, List
from app.pb_clients.libros import db_get_all_para_recomendador, db_get_libro
from app.interfaces.libro_expert import LibroExpertSystem

_expert_instance: Optional[LibroExpertSystem] = None


def get_expert_system() -> LibroExpertSystem:
    """
    Devuelve la instancia singleton del sistema experto.
    Se entrena la primera vez que se llama (lazy init).
    """
    global _expert_instance
    if _expert_instance is None:
        libros = db_get_all_para_recomendador()
        _expert_instance = LibroExpertSystem(libros)
    return _expert_instance


def reset_expert_system():
    """Fuerza re-entrenamiento en la próxima llamada a get_expert_system()."""
    global _expert_instance
    _expert_instance = None


def get_libro_completo(pk_id_libro: int) -> Dict[str, Any]:
    """Obtiene el libro completo de la BD y lo convierte a dict."""
    libro = db_get_libro(pk_id_libro)
    if libro is None:
        raise ValueError(f"Libro con pk_id_libro={pk_id_libro} no encontrado.")
    if hasattr(libro, "dict"):
        return libro.dict()
    return dict(libro)


def hidratar_top3(top3_raw: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Recibe [{ pk_id_libro, confianza }, ...]
    Devuelve [{ pk_id_libro, confianza, libro: {...} }, ...]
    """
    resultado = []
    for item in top3_raw:
        try:
            libro = get_libro_completo(item["pk_id_libro"])
        except Exception:
            libro = None
        resultado.append({
            "pk_id_libro": item["pk_id_libro"],
            "confianza": item["confianza"],
            "libro": libro,
        })
    return resultado
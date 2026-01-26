from sklearn.preprocessing import OneHotEncoder
from datetime import datetime
from typing import List


def get_ml_recomendaciones(historial_libros: List) -> List:
    """
    "pk_id_prestamo": prestamo.pk_id_prestamo,
    "titulo": titulo_libro,
    "autor": autor,
    "descripcion": descripcion, 
    "genero": genero_lista,
    "fecha_prestamo": prestamo.fecha_prestamo,
    "fecha_entrega": prestamo.fecha_entrega,
    "estatus_entrega": prestamo.estatus_entrega,
    """

    libros = []
    for libro in historial_libros:
        print(libro["genero"])

        _libro = {
            "autor": libro["autor"],
            "dias_prestamo": (
                (datetime.fromisoformat(libro["fecha_entrega"]) -
                datetime.fromisoformat(libro["fecha_prestamo"])).days
                if libro["fecha_entrega"] is not None and libro["fecha_prestamo"] is not None
                else "No Entregado Aún"
            ),          
            "estrellas": 0 if not libro["estrellas"] else libro["estrellas"],
            "generos": libro["genero"],
        }
        libros.append(_libro)
    return libros
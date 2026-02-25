from typing import Dict, Any, Optional, List
from app.core.config import settings
from app.core.auth import db_get_client

from app.models.db_models import Libro

def db_get_recomendaciones(fk_id_usuario: str) -> List[Libro]:
    client = db_get_client()
    base_url = settings.POCKETBASE_URL_IMAGENES
    collection_id = "pbc_2270877598"
    libros = []
    recomendaciones = client.collection("RecomendacionesUsuarios").get_first_list_item(
        f'fk_id_usuario = "{fk_id_usuario}"',
        {"expand": "libros"}
    )

    if recomendaciones is None:
        return libros

    libros_ = recomendaciones.expand.get("libros", [])
    #print(range(len(libros_)))
    for i in range(len(libros_)):
        libro_ = Libro(
                 id=libros_[i].id,
                 pk_id_libro=libros_[i].pk_id_libro,
                 titulo=libros_[i].titulo,
                 autor=libros_[i].autor,
                 descripcion=libros_[i].descripcion,
                 fecha_publicacion=libros_[i].fecha_publicacion,
                 ruta_img=f"{base_url}/api/files/{collection_id}/{libros_[i].id}/{libros_[i].ruta_img}",
                 copias=libros_[i].copias,
                 fk_id_departamento=libros_[i].fk_id_departamento,
                 fk_id_genero=libros_[i].fk_id_genero,
                 estrellas=int(libros_[i].estrellas) if libros_[i].estrellas else 0,
                 created_at=libros_[i].created,
                 updated_at=libros_[i].updated,
            )
        libros.append(libro_)
        #print(f"indice: {i}: {libros_[i]}")
    
    return libros
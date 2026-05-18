from typing import Dict, List

from requests.models import Response

from app.core.auth import db_get_client
from app.models.db_models import CopiaLibro, Libro
from app.pb_clients.pb_utils import actualizar_copias_libros ,estatus_prestamo, db_get_count_copias_libros

from app.core.config import settings

from app.pb_clients.libros import (
    db_update_libro
)

def db_get_last_id_copia_libro() -> int:
    client = db_get_client()
    last_copia = client.collection("CopiasLibro").get_list(
        page=1,
        per_page=1,
        query_params={
            "sort": "-pk_id_copia"
        }
    )
    if not last_copia.items:
        return 0
    return last_copia.items[0].pk_id_copia

def db_create_copia_libro(copia_libro: CopiaLibro) -> CopiaLibro:
    client = db_get_client()
    last_copia = db_get_last_id_copia_libro()
    copia = copia_libro.model_dump(mode="json")
    record = client.collection("CopiasLibro").create({
                                            "pk_id_copia": last_copia + 1,
                                            "fk_id_libro": copia_libro.fk_id_libro,
                                            "isbn": copia_libro.isbn,
                                            "rfid_tag": copia_libro.rfid_tag,
                                            "disponibilidad": copia_libro.disponibilidad,
                                            })


    

    libro = client.collection('Libros').get_one(copia['fk_id_libro'])

    print(libro.copias)

    libro_actualizado = Libro(
        id=libro.id,
        pk_id_libro=libro.pk_id_libro,
        titulo=libro.titulo,
        autor=libro.autor,
        descripcion= libro.descripcion,
        fecha_publicacion=libro.fecha_publicacion,
        ruta_img=None,
        copias=db_get_count_copias_libros(libro.id),
        fk_id_departamento=libro.fk_id_departamento,
        fk_id_genero=libro.fk_id_genero,
        estrellas=int(libro.estrellas),
        created_at=libro.created,
        updated_at=None,
    )

    db_update_libro(libro_actualizado)

    return CopiaLibro(
        id=record.id,
        pk_id_copia=record.pk_id_copia,
        fk_id_libro=record.fk_id_libro,
        isbn=record.isbn,
        rfid_tag=record.rfid_tag,
        disponibilidad=record.disponibilidad,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


def db_get_copia_libro(pk_id_copia_libro: int) -> CopiaLibro:
    client = db_get_client()
    record = client.collection("CopiasLibro").get_first_list_item(
        f'pk_id_copia = {pk_id_copia_libro}'
    )
    return CopiaLibro(
        id=record.id,
        pk_id_copia=record.pk_id_copia,
        fk_id_libro=record.fk_id_libro,
        isbn=record.isbn,
        rfid_tag=record.rfid_tag,
        disponibilidad=record.disponibilidad,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )

def db_get_ultimo_id_copia() -> int:
    client = db_get_client()
    last_copy = client.collection("CopiasLibro").get_list(
        page=1,
        per_page=1,
        query_params={
            "sort": "-pk_id_copia",
        }
    )
    if not last_copy.items:
        return 0
    return last_copy.items[0].pk_id_copia

def db_get_all_copies() -> List:
    base_url = f"{settings.POCKETBASE_URL_IMAGENES}" #"http://localhost:8090"
    collection_id = "pbc_2270877598"
    client = db_get_client()
    record = client.collection("CopiasLibro").get_full_list(
        15,
        {"expand": "fk_id_libro"}
    )

    # record[0].expand.get("fk_id_libro").autor

    copias_list = []
    for r in record:
        copias_list.append(
            {
                "id": r.id,
                "pk_id_copia": r.pk_id_copia,
                "libro":{
                    "autor": r.expand.get("fk_id_libro").autor,
                    "titulo": r.expand.get("fk_id_libro").titulo,
                    "ruta_img": f"{base_url}/api/files/{collection_id}/{r.expand.get('fk_id_libro').id}/{r.expand.get('fk_id_libro').ruta_img}"
                },
                "fk_id_libro": r.fk_id_libro,
                "isbn": r.isbn,
                "rfid_tag": r.rfid_tag,
                "disponibilidad": r.disponibilidad,
            }
        )
    return copias_list

def db_get_copias_paginadas(limit, offset, q=None) -> Dict:
    # 1. Cálculo de página (PocketBase usa base 1)
    page = (offset // limit) + 1

    base_url = f"{settings.POCKETBASE_URL_IMAGENES}"
    collection_id_libros = "pbc_2270877598" # ID de la colección 'Libros'
    client = db_get_client()

    query_params = {
        "expand": "fk_id_libro"
    }

    # 2. Corregir el filtro para usar campos expandidos
    if q:
        q = q.strip()
        # IMPORTANTE: Usamos fk_id_libro.campo para buscar en la relación
        query_params["filter"] = f'fk_id_libro.titulo ~ "{q}" || fk_id_libro.autor ~ "{q}"'

    try:
        record = client.collection("CopiasLibro").get_list(
            page=page,
            per_page=limit,
            query_params=query_params
        )
    except Exception as e:
        print(f"Error en PocketBase: {e}")
        return {"items": [], "total": 0}

    copias_list = []

    for r in record.items:
        # Extraer el objeto expandido de forma segura
        libro_data = r.expand.get("fk_id_libro") if r.expand else None
        
        # El objeto expandido en el SDK de Python suele ser un objeto Record o un Dict
        # Si es un objeto Record, accedemos con .campo, si es dict con .get()
        # Asumiendo que el SDK devuelve objetos Record en el expand:
        
        copias_list.append(
            {
                "id": r.id,
                "pk_id_copia": getattr(r, "pk_id_copia", None),
                "libro": {
                    "autor": getattr(libro_data, "autor", None) if libro_data else "Desconocido",
                    "titulo": getattr(libro_data, "titulo", None) if libro_data else "Sin título",
                    "ruta_img": (
                        f"{base_url}/api/files/{collection_id_libros}/{libro_data.id}/{libro_data.ruta_img}"
                        if libro_data and getattr(libro_data, "ruta_img", None)
                        else None
                    )
                },
                "fk_id_libro": r.fk_id_libro,
                "isbn": getattr(r, "isbn", None),
                "rfid_tag": getattr(r, "rfid_tag", None),
                "disponibilidad": getattr(r, "disponibilidad", False),
            }
        )

    return {
        "items": copias_list,
        "total": record.total_items
    }

def db_get_copia_libro_rfid(rfid: str) -> Dict:
    base_url = f"{settings.POCKETBASE_URL_IMAGENES}"
    collection_id_libros = "pbc_2270877598"
    client = db_get_client()

    # Buscar la copia del libro por el RFID
    record = client.collection("CopiasLibro").get_first_list_item(
        f'rfid_tag = "{rfid}"'
    )

    # Ahora obtener los datos del libro relacionado
    libro = client.collection("Libros").get_one(record.fk_id_libro)

    # Construir el formato de salida
    response = {
            "id": record.id,
            "pk_id_copia": record.pk_id_copia,
            "disponibilidad": record.disponibilidad,
            "rfid_tag": record.rfid_tag,
            "titulo": libro.titulo,
            "descripcion": libro.descripcion,
            "fecha_publicacion": libro.fecha_publicacion,
            "estrellas": libro.estrellas,
            "autor": libro.autor,
            "isbn": record.isbn,
            "ruta_img": (
                        f"{base_url}/api/files/{collection_id_libros}/{libro.id}/{libro.ruta_img}"
                        if libro and getattr(libro, "ruta_img", None)
                        else None
                    )
        }

    return response

def db_update_stat_copia_libro_prestado(pk_id_copia: int) -> bool:
    client = db_get_client()

    # Buscar la copia del libro por el RFID
    record = client.collection("CopiasLibro").get_first_list_item(
        f'pk_id_copia = "{pk_id_copia}"'
    )

    actualizar_copias_libros(record.fk_id_libro)

    # Construir el formato de salida

    copia_libro = CopiaLibro(
        id=record.id,
        pk_id_copia=record.pk_id_copia,
        fk_id_libro=record.fk_id_libro,
        isbn=record.isbn,
        rfid_tag=record.rfid_tag,
        disponibilidad=False,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )

    updated = client.collection("CopiasLibro").update(
        copia_libro.id, copia_libro.model_dump(mode="json")
    )

    return updated

def db_update_stat_copia_libro_devuelto(pk_id_copia: int) -> bool:
    client = db_get_client()

    # Buscar la copia del libro por el RFID
    record = client.collection("CopiasLibro").get_first_list_item(
        f'pk_id_copia = "{pk_id_copia}"'
    )
    
    estatus_prestamo(record.id)

    # Construir el formato de salida

    copia_libro = CopiaLibro(
        id=record.id,
        pk_id_copia=record.pk_id_copia,
        fk_id_libro=record.fk_id_libro,
        isbn=record.isbn,
        rfid_tag=record.rfid_tag,
        disponibilidad=True,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )

    updated = client.collection("CopiasLibro").update(
        copia_libro.id, copia_libro.model_dump(mode="json")
    )

    return updated


def db_update_copia_libro(copia_libro: CopiaLibro) -> CopiaLibro:
    client = db_get_client()
    updated = client.collection("CopiasLibro").update(
        copia_libro.id, copia_libro.model_dump(mode="json")
    )

    actualizar_copias_libros(updated.fk_id_libro)
    
    return CopiaLibro(
        id=updated.id,
        pk_id_copia=updated.pk_id_copia,
        fk_id_libro=updated.fk_id_libro,
        isbn=updated.isbn,
        rfid_tag=updated.rfid_tag,
        disponibilidad=updated.disponibilidad,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
    )


def db_delete_copia_libro(pk_id_copia: int) -> Response:
    client = db_get_client()
    copia = client.collection("CopiasLibro").get_first_list_item(
        f'pk_id_copia = "{pk_id_copia}"'
    )

    # Optional: delete related Prestamos if necessary
    prestamos = client.collection("Prestamos").get_full_list(
        query_params={"filter": f'fk_id_copia="{copia.id}"'}
    )

    for prestamo in prestamos:
        client.collection("Prestamos").delete(prestamo.id)

    status = client.collection("CopiasLibro").delete(copia.id)

    actualizar_copias_libros(copia.fk_id_libro)

    return status


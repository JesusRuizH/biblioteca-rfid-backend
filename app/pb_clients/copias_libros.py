from typing import Dict, List

from requests.models import Response

from app.core.auth import db_get_client
from app.models.db_models import CopiaLibro, Libro

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
        copias=int(libro.copias)+1 if libro.copias is not None else 0,
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
    base_url = "http://localhost:8090"
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
    page = (offset // limit) + 1

    base_url = "http://localhost:8090"
    collection_id = "pbc_2270877598"
    client = db_get_client()

    query_params = {
        "expand": "fk_id_libro"
    }

    if q:
        q = q.strip()
        query_params["filter"] = f'rfid_tag ~ "{q}" || isbn ~ "{q}"'

    record = client.collection("CopiasLibro").get_list(
        page=page,
        per_page=limit,
        query_params=query_params
    )

    copias_list = []

    for r in record.items:
        libro = r.expand.get("fk_id_libro") if r.expand else None

        copias_list.append(
            {
                "id": r.id,
                "pk_id_copia": r.pk_id_copia,
                "libro": {
                    "autor": libro.autor if libro else None,
                    "titulo": libro.titulo if libro else None,
                    "ruta_img": (
                        f"{base_url}/api/files/{collection_id}/{libro.id}/{libro.ruta_img}"
                        if libro and libro.ruta_img
                        else None
                    )
                },
                "fk_id_libro": r.fk_id_libro,
                "isbn": r.isbn,
                "rfid_tag": r.rfid_tag,
                "disponibilidad": r.disponibilidad,
            }
        )

    return {
        "items": copias_list,
        "total": record.total_items
    }


def db_get_copia_libro_rfid(rfid: str) -> Dict:
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
            "autor": libro.autor,
            "isbn": record.isbn,
        }

    return response

def db_update_stat_copia_libro_prestado(pk_id_copia: int) -> bool:
    client = db_get_client()

    # Buscar la copia del libro por el RFID
    record = client.collection("CopiasLibro").get_first_list_item(
        f'pk_id_copia = "{pk_id_copia}"'
    )

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

    libro = client.collection('Libros').get_one(copia.fk_id_libro)

    libro_actualizado = Libro(
        id=libro.id,
        pk_id_libro=libro.pk_id_libro,
        titulo=libro.titulo,
        autor=libro.autor,
        descripcion= libro.descripcion,
        fecha_publicacion=libro.fecha_publicacion,
        ruta_img=None,
        copias=int(libro.copias)-1 if libro.copias is not None else 0,
        fk_id_departamento=libro.fk_id_departamento,
        fk_id_genero=libro.fk_id_genero,
        estrellas=int(libro.estrellas),
        created_at=libro.created,
        updated_at=None,
    )

    db_update_libro(libro_actualizado)

    for prestamo in prestamos:
        client.collection("Prestamos").delete(prestamo.id)

    return client.collection("CopiasLibro").delete(copia.id)

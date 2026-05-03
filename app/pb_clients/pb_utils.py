from typing import List
from collections import Counter
from app.models.db_models import Libro, Prestamo

from app.core.auth import db_get_client

from app.pb_clients.libros import (
    db_update_libro
)
from app.core.config import settings


def db_get_top_libros(top: int) -> List:
    client = db_get_client()
    records = client.collection("Prestamos").get_full_list(
        200,
        {"expand": "fk_id_copia, fk_id_copia.fk_id_libro"}
    )
    conteo_libros = []
    for record in records:
        copias = record.expand.get("fk_id_copia")
        libros = copias.expand.get("fk_id_libro")
        conteo_libros.append(libros.id)
        #print(libros.titulo)

    conteo = Counter(conteo_libros)
    top_libros = []
    cont = 0

    base_url = settings.POCKETBASE_URL_IMAGENES
    collection_id = "pbc_2270877598"

    for key, value in conteo.items():
        if cont < top:
            libro = client.collection("Libros").get_first_list_item(
                f'id="{key}"',
                {"expand": "fk_id_departamento, fk_id_genero"}
            )
            nombre_departamento = ""
            departamento_numero = ""
            genero_nombre = []
            departamento = libro.expand.get("fk_id_departamento")
            generos_list = libro.expand.get("fk_id_genero")
            if departamento:
                nombre_departamento = departamento.nombre
                departamento_numero = departamento.numero

            if generos_list:
                for genero in generos_list:
                    genero_nombre.append(genero.genero)

            libro_top = {
                "pk_id_libro": libro.pk_id_libro,
                "titulo": libro.titulo,
                "autor": libro.autor,
                "descripcion": libro.descripcion,
                "fecha_publicacion": libro.fecha_publicacion,
                "ruta_img": f"{base_url}/api/files/{collection_id}/{libro.id}/{libro.ruta_img}",
                "copias": libro.copias,
                "genero": genero_nombre,
                "estrellas": libro.estrellas,
                "departamento_numero": departamento_numero,
                "departamento": nombre_departamento,
                "veces_prestado": value
            }
            top_libros.append(libro_top)
            cont += 1
        else:
            break
    return top_libros

def actualizar_copias_libros(fk_id_libro: str) -> Libro: 
    client = db_get_client()
    libro = client.collection('Libros').get_one(fk_id_libro)

    libro_actualizado = Libro(
        id=libro.id,
        pk_id_libro=libro.pk_id_libro,
        titulo=libro.titulo,
        autor=libro.autor,
        descripcion= libro.descripcion,
        fecha_publicacion=libro.fecha_publicacion,
        ruta_img=None,
        copias=db_get_count_copias_libros(fk_id_libro),
        fk_id_departamento=libro.fk_id_departamento,
        fk_id_genero=libro.fk_id_genero,
        estrellas=int(libro.estrellas),
        created_at=libro.created,
        updated_at=None,
    )

    db_update_libro(libro_actualizado)


    return libro_actualizado

def actualizar_copias_libros(fk_id_libro: str) -> Libro: 
    client = db_get_client()
    libro = client.collection('Libros').get_one(fk_id_libro)

    libro_actualizado = Libro(
        id=libro.id,
        pk_id_libro=libro.pk_id_libro,
        titulo=libro.titulo,
        autor=libro.autor,
        descripcion= libro.descripcion,
        fecha_publicacion=libro.fecha_publicacion,
        ruta_img=None,
        copias=db_get_count_copias_libros(fk_id_libro),
        fk_id_departamento=libro.fk_id_departamento,
        fk_id_genero=libro.fk_id_genero,
        estrellas=int(libro.estrellas),
        created_at=libro.created,
        updated_at=None,
    )
    db_update_libro(libro_actualizado)

    return libro_actualizado

from datetime import datetime

def estatus_prestamo(pk_id_copia: str) -> Prestamo: 
    client = db_get_client()
    
    print(pk_id_copia)
    # 1. Obtenemos el registro más reciente
    record = client.collection("Prestamos").get_first_list_item(
        f'fk_id_copia = "{pk_id_copia}"',
        {
            "sort": "-created_at",
        }
    )

    print(record)

    # 2. Generamos la fecha actual en formato ISO (ej. 2024-05-20T14:30:00)
    # .isoformat() incluye la 'T' por defecto
    fecha_hoy = datetime.now().isoformat()

    # 3. Creamos el objeto con la nueva fecha de entrega
    prestamo_actualizado = Prestamo(
        id=record.id,
        pk_id_prestamo=record.pk_id_prestamo,
        fk_id_copia=record.fk_id_copia,
        fk_id_usuario=record.fk_id_usuario,
        fecha_prestamo=record.fecha_prestamo,
        fecha_entrega=fecha_hoy,  # <--- Aplicada aquí
        dias_restantes=0,
        estatus_entrega=True
    )

    db_update_prestamo(prestamo_actualizado)

    return prestamo_actualizado

def db_update_prestamo(prestamo: Prestamo) -> Prestamo:
    client = db_get_client()
    record = client.collection("Prestamos").update(
        prestamo.id, prestamo.model_dump(mode="json")
    )

    return Prestamo(
        id=record.id,
        pk_id_prestamo=record.pk_id_prestamo,
        fk_id_copia=record.fk_id_copia,
        fk_id_usuario=record.fk_id_usuario,
        fecha_prestamo=record.fecha_prestamo,
        fecha_entrega=record.fecha_entrega,
        dias_restantes=record.dias_restantes,
        estatus_entrega=record.estatus_entrega,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )

def db_get_count_copias_libros(fk_id_libro) -> int:
    client = db_get_client()
    if not client:
        return 0

    try:
        # We request only 1 item per page (the minimum) 
        # because we only care about the 'total_items' property.
        result = client.collection("CopiasLibro").get_list(
            page=1,
            per_page=1,
            query_params={
                "filter": f'fk_id_libro="{fk_id_libro}" && disponibilidad=True'
            }
        )
        #print(result.total_items)
        return result.total_items
    except Exception as e:
        print(f"Error al contar copias: {e}")
        return 0
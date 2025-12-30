import base64
import os
import re
from typing import List

import requests

from app.core.auth import db_get_client
from app.models.db_models import Libro
from requests.models import Response
from pocketbase.client import FileUpload

import os
import re
import base64
import requests
from pocketbase.client import FileUpload

def db_create_libro(libro: Libro):
    client = db_get_client()
    direccion_img = libro.ruta_img
    file_upload = None

    if not direccion_img:
        raise ValueError("No se recibió ninguna imagen")

    # Caso 1: URL externa (http/https)
    if direccion_img.startswith("http://") or direccion_img.startswith("https://"):
        response = requests.get(direccion_img)
        response.raise_for_status()
        filename = os.path.basename(direccion_img) or "image.jpg"
        file_upload = FileUpload((filename, response.content))

    # Caso 2: Imagen en Base64 (cuando viene del front)
    elif direccion_img.startswith("data:image/"):
        try:
            header, encoded = direccion_img.split(",", 1)
            ext = re.search(r"data:image/(.*);base64", header).group(1)
            filename = f"upload.{ext}"
            img_bytes = base64.b64decode(encoded)
            file_upload = FileUpload((filename, img_bytes))
        except Exception as e:
            raise ValueError(f"Error procesando imagen base64: {e}")

    # Caso 3: archivo local
    else:
        if not os.path.isfile(direccion_img):
            raise FileNotFoundError(f"No existe el archivo local: {direccion_img}")
        filename = os.path.basename(direccion_img)
        with open(direccion_img, "rb") as f:
            file_upload = FileUpload((filename, f.read()))

    # ⚡️ Si es string simple, conviértelo a lista
    generos = libro.fk_id_genero
    if isinstance(generos, str) and generos.strip() != "":
        generos = [generos]
    elif not generos:
        generos = []

    # Crear registro en PocketBase
    record = client.collection("Libros").create(
        {
            "pk_id_libro": libro.pk_id_libro,
            "titulo": libro.titulo,
            "autor": libro.autor,
            "fecha_publicacion": libro.fecha_publicacion,
            "ruta_img": file_upload,  # campo tipo file en PB
            "copias": libro.copias,
            "fk_id_departamento": libro.fk_id_departamento,
            "fk_id_genero": generos,   # 👈 ahora siempre es array
            "created_at": libro.created_at,
            "updated_at": libro.updated_at,
        }
    )

    # Devolver objeto Libro con los datos guardados en PB
    return Libro(
        id=record.id,
        pk_id_libro=record.pk_id_libro,
        titulo=record.titulo,
        autor=record.autor,
        fecha_publicacion=record.fecha_publicacion,
        ruta_img=record.ruta_img,   # 👉 ya es URL pública de PB
        copias=record.copias,
        fk_id_departamento=record.fk_id_departamento,
        fk_id_genero=record.fk_id_genero,  # 👉 PB devuelve lista
        created_at=record.created,
        updated_at=record.updated,
    )



def db_get_libro(pk_id_libro: int) -> Libro:
    client = db_get_client()
    record = client.collection("Libros").get_first_list_item(
        f'pk_id_libro = {pk_id_libro}',
    )
    return Libro(
        id=record.id,
        pk_id_libro=record.pk_id_libro,
        titulo=record.titulo,
        autor=record.autor,
        fecha_publicacion=record.fecha_publicacion,
        ruta_img=record.ruta_img,
        copias=record.copias,
        fk_id_departamento=record.fk_id_departamento,
        fk_id_genero=record.fk_id_genero,
        created_at=record.created,
        updated_at=record.updated,
    )

def db_update_libro(libro: Libro):
    client = db_get_client()
    direccion_img = libro.ruta_img
    file_upload = None

    # Si no viene imagen, no forzamos error, solo no actualizamos ruta_img
    if direccion_img:
        # Caso 1: URL externa (http/https)
        if direccion_img.startswith("http://") or direccion_img.startswith("https://"):
            response = requests.get(direccion_img)
            response.raise_for_status()
            filename = os.path.basename(direccion_img) or "image.jpg"
            file_upload = FileUpload((filename, response.content))

        # Caso 2: Imagen en Base64
        elif direccion_img.startswith("data:image/"):
            try:
                header, encoded = direccion_img.split(",", 1)
                ext = re.search(r"data:image/(.*);base64", header).group(1)
                filename = f"upload.{ext}"
                img_bytes = base64.b64decode(encoded)
                file_upload = FileUpload((filename, img_bytes))
            except Exception as e:
                raise ValueError(f"Error procesando imagen base64: {e}")

        # Caso 3: archivo local
        else:
            if not os.path.isfile(direccion_img):
                raise FileNotFoundError(f"No existe el archivo local: {direccion_img}")
            filename = os.path.basename(direccion_img)
            with open(direccion_img, "rb") as f:
                file_upload = FileUpload((filename, f.read()))

    # ⚡️ Normalizar géneros: siempre lista
    generos = libro.fk_id_genero
    if isinstance(generos, str) and generos.strip() != "":
        generos = [generos]
    elif not generos:
        generos = []

    # Construir payload para update
    payload = {
        "pk_id_libro": libro.pk_id_libro,
        "titulo": libro.titulo,
        "autor": libro.autor,
        "fecha_publicacion": libro.fecha_publicacion,
        "copias": libro.copias,
        "fk_id_departamento": libro.fk_id_departamento,
        "fk_id_genero": generos,
        "updated_at": libro.updated_at,
    }

    # Solo actualizamos imagen si vino
    if file_upload:
        payload["ruta_img"] = file_upload

    # 🔹 Hacer update en PocketBase
    record = client.collection("Libros").update(libro.id, payload)

    # Retornar objeto Libro con valores de PB
    return Libro(
        id=record.id,
        pk_id_libro=record.pk_id_libro,
        titulo=record.titulo,
        autor=record.autor,
        fecha_publicacion=record.fecha_publicacion,
        ruta_img=record.ruta_img,
        copias=record.copias,
        fk_id_departamento=record.fk_id_departamento,
        fk_id_genero=record.fk_id_genero,
        created_at=record.created,
        updated_at=record.updated,
    )

def db_delete_libro(pk_id_libro: int) -> Response:
    client = db_get_client()
    libro = client.collection("Libros").get_first_list_item(
        f'pk_id_libro="{pk_id_libro}"'
    )
    copia_libro = client.collection("CopiasLibro").get_full_list(
        query_params={
            "filter": f'fk_id_libro="{libro.id}"'
        }
    )
    for record_copia_libro in copia_libro:
        prestamo = client.collection("Prestamos").get_full_list(
            query_params={
                "filter": f'fk_id_copia="{record_copia_libro.id}"'
            }
        )
        for record_prestamo in prestamo:
            client.collection("Prestamos").delete(record_prestamo.id)
        client.collection("CopiasLibro").delete(record_copia_libro.id)

    return client.collection("Libros").delete(libro.id)


def db_get_all_libros(cantidad: int) -> List:
    client = db_get_client()
    records = client.collection("Libros").get_full_list(
        cantidad,
        {"expand": "fk_id_departamento, fk_id_genero",}
    )
    libros = []
    for record in records:
        base_url = "http://localhost:8090"
        collection_id = "pbc_2270877598"
        nombre_departamento = ""
        departamento_numero = ""
        genero_nombre = []
        departamento = record.expand.get("fk_id_departamento")
        generos_list = record.expand.get("fk_id_genero")
        if departamento:
            nombre_departamento = departamento.nombre
            departamento_numero = departamento.numero

        if generos_list:
            for genero in generos_list:
                genero_nombre.append(genero.genero)

        libro = {
            "id": record.id,
            "pk_id_libro": record.pk_id_libro,
            "titulo":  record.titulo,
            "autor": record.autor,
            "fecha_publicacion": record.fecha_publicacion,
            "ruta_img": f"{base_url}/api/files/{collection_id}/{record.id}/{record.ruta_img}",
            "copias": record.copias,
            "genero": genero_nombre,
            "departamento_numero": departamento_numero,
            "departamento": nombre_departamento,
        }
        libros.append(libro)
    return libros

def db_get_last_id_libro() -> int:
    client = db_get_client()
    last_book = client.collection("Libros").get_list(
        page=1,
        per_page=1,
        query_params={
            "sort": "-pk_id_libro"
        }
    )
    if not last_book.items:
        return 0
    return last_book.items[0].pk_id_libro

def db_get_all() -> List[Libro]:
    base_url = "http://localhost:8090"
    collection_id = "pbc_2270877598"
    client = db_get_client()
    record = client.collection("Libros").get_full_list()
    usuarios_list = []
    for r in record:
        usuarios_list.append(
             Libro(
                 id=r.id,
                 pk_id_libro=r.pk_id_libro,
                 titulo=r.titulo,
                 autor=r.autor,
                 fecha_publicacion=r.fecha_publicacion,
                 ruta_img=f"{base_url}/api/files/{collection_id}/{r.id}/{r.ruta_img}",
                 copias=r.copias,
                 fk_id_departamento=r.fk_id_departamento,
                 fk_id_genero=r.fk_id_genero,
                 created_at=r.created,
                 updated_at=r.updated,
            )
        )
    return usuarios_list
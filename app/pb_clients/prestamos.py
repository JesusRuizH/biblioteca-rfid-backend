from collections import Counter
from datetime import datetime
from typing import Dict

from requests.models import Response

from app.core.auth import db_get_client
from app.models.db_models import Prestamo
from app.pb_clients.usuarios import db_get_usuario

from app.pb_clients.libros import *

import time

from app.core.config import settings

LIBROS_CACHE: List = []
CACHE_LAST_UPDATE = 0
CACHE_TTL = 60  # segundos (ej: 1 minuto)

def db_create_prestamo(prestamo: Prestamo) -> Prestamo:
    client = db_get_client()
    record = client.collection("Prestamos").create(prestamo.model_dump(mode="json"))

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


def db_get_prestamo(pk_id_prestamo: int) -> Prestamo:
    client = db_get_client()
    record = client.collection("Prestamos").get_first_list_item(
        f'pk_id_prestamo = {pk_id_prestamo}'
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
                "departamento_numero": departamento_numero,
                "departamento": nombre_departamento,
                "veces_prestado": value
            }
            top_libros.append(libro_top)
            cont += 1
        else:
            break
    return top_libros



def refresh_libros_cache():
    global LIBROS_CACHE, CACHE_LAST_UPDATE

    libros = db_get_top_libros(10)  # TU FUNCIÓN
    LIBROS_CACHE = libros
    CACHE_LAST_UPDATE = time.time()

def get_libros_cache():
    if time.time() - CACHE_LAST_UPDATE > CACHE_TTL:
        refresh_libros_cache()

    return LIBROS_CACHE


def db_get_mis_prestamos_pendientes(pk_id_usuario: int) -> List:
    client = db_get_client()
    usuario = db_get_usuario(pk_id_usuario)
    prestamos = client.collection("Prestamos").get_list(
        1,
        20,
        {
            "filter": f'fk_id_usuario = "{usuario.id}" && estatus_entrega = false',
            "expand": "fk_id_copia.fk_id_libro"
        }
    )
    mis_prestamos = []

    for prestamo in prestamos.items:
        titulo_libro = ""
        copia = prestamo.expand.get("fk_id_copia")
        if copia:
            libro = copia.expand.get("fk_id_libro")
            if libro:
                titulo_libro = libro.titulo


        libro_top = {
            "pk_id_prestamo": prestamo.pk_id_prestamo,
            "titulo": titulo_libro,
            "fecha_prestamo": prestamo.fecha_entrega,
            "fecha_entrega": prestamo.fecha_entrega,
        }
        mis_prestamos.append(libro_top)
    return mis_prestamos

def db_get_historial_prestamos(pk_id_usuario: int) -> List:
    client = db_get_client()
    usuario = db_get_usuario(pk_id_usuario)
    prestamos = client.collection("Prestamos").get_list(
        1,
        20,
        {
            "filter": f'fk_id_usuario = "{usuario.id}"',
            "expand": "fk_id_copia.fk_id_libro.fk_id_genero"
        }
    )
    mis_prestamos = []

    for prestamo in prestamos.items:
        titulo_libro = ""
        autor = ""
        genero_lista = []
        copia = prestamo.expand.get("fk_id_copia")
        if copia:
            libro = copia.expand.get("fk_id_libro")
            if libro:
                titulo_libro = libro.titulo
                autor = libro.autor
                generos = libro.expand.get("fk_id_genero")
                if generos:
                    for genero in generos:
                        genero_lista.append(genero.genero)


        libros_prestados = {
            "pk_id_prestamo": prestamo.pk_id_prestamo,
            "titulo": titulo_libro,
            "autor": autor,
            "genero": genero_lista,
            "fecha_prestamo": prestamo.fecha_prestamo,
            "fecha_entrega": prestamo.fecha_entrega,
            "estatus_entrega": prestamo.estatus_entrega,
        }
        mis_prestamos.append(libros_prestados)
    return mis_prestamos

def db_get_mis_recomendaciones(pk_id_usuario: int) -> List: 
    # Basado en el id del usuario retornaremos un conjunto de recomendaciones basadas en Basic ML y arboles de decisión
    client = db_get_client()
    usuario = db_get_usuario(pk_id_usuario)
    prestamos = client.collection("Prestamos").get_list(
        1,
        20,
        {
            "filter": f'fk_id_usuario = "{usuario.id}"',
            "expand": "fk_id_copia.fk_id_libro.fk_id_genero"
        }
    )
    mis_prestamos = []

    for prestamo in prestamos.items:
        titulo_libro = ""
        autor = ""
        descripcion = ""
        genero_lista = []
        copia = prestamo.expand.get("fk_id_copia")
        if copia:
            libro = copia.expand.get("fk_id_libro")
            if libro:
                titulo_libro = libro.titulo
                autor = libro.autor
                descripcion = libro.descripcion
                generos = libro.expand.get("fk_id_genero")
                if generos:
                    for genero in generos:
                        genero_lista.append(genero.genero)


        libros_prestados = {
            "pk_id_prestamo": prestamo.pk_id_prestamo,
            "titulo": titulo_libro,
            "autor": autor,
            "descripcion": descripcion, 
            "genero": genero_lista,
            "fecha_prestamo": prestamo.fecha_prestamo,
            "fecha_entrega": prestamo.fecha_entrega,
            "estatus_entrega": prestamo.estatus_entrega,
        }
        mis_prestamos.append(libros_prestados)


    return mis_prestamos


def db_get_total_prestamos() -> int:
    client = db_get_client()
    result = client.collection("Prestamos").get_list(1, 1)
    total_count = result.total_items
    print("Total Prestamos:", total_count)

    return total_count


def db_get_historial_prestamos_admin(cantidad: int) -> List:
    client = db_get_client()
    prestamos = client.collection("Prestamos").get_list(
        1,
        cantidad,
        {
            "expand": "fk_id_copia.fk_id_libro.fk_id_genero",
            "sort": "-created_at"
        }
    )
    mis_prestamos = []
    for prestamo in prestamos.items:
        titulo_libro = ""
        autor = ""
        genero_lista = []
        copia = prestamo.expand.get("fk_id_copia")
        if copia:
            libro = copia.expand.get("fk_id_libro")
            if libro:
                titulo_libro = libro.titulo
                autor = libro.autor
                generos = libro.expand.get("fk_id_genero")
                if generos:
                    for genero in generos:
                        genero_lista.append(genero.genero)


        libros_prestados = {
            "pk_id_prestamo": prestamo.pk_id_prestamo,
            "titulo": titulo_libro,
            "autor": autor,
            "genero": genero_lista,
            "fecha_prestamo": prestamo.fecha_prestamo,
            "fecha_entrega": prestamo.fecha_entrega,
            "estatus_entrega": prestamo.estatus_entrega,
        }
        mis_prestamos.append(libros_prestados)
    return mis_prestamos

def db_get_last_id_prestamos() -> int:
    client = db_get_client()
    last_prestamo = client.collection("Prestamos").get_list(
        page=1,
        per_page=1,
        query_params={
            "sort": "-pk_id_prestamo"
        }
    )
    if not last_prestamo.items:
        return 0
    return last_prestamo.items[0].pk_id_prestamo

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

def db_get_generos_leidos(pk_id_usuario: int) -> Dict:
    client = db_get_client()
    usuario = db_get_usuario(pk_id_usuario)
    prestamos = client.collection("Prestamos").get_list(
        1,
        20,
        {
            "filter": f'fk_id_usuario = "{usuario.id}"',
            "expand": "fk_id_copia.fk_id_libro.fk_id_genero"
        }
    )

    genero_lista = []
    for prestamo in prestamos.items:
        copia = prestamo.expand.get("fk_id_copia")
        if copia:
            libro = copia.expand.get("fk_id_libro")
            if libro:
                generos = libro.expand.get("fk_id_genero")
                if generos:
                    for genero in generos:
                        genero_lista.append(genero.genero)

    conteo_generos = Counter(genero_lista)

    return conteo_generos

def db_get_generos_leidos_admin() -> List:
    client = db_get_client()
    prestamos = client.collection("Prestamos").get_list(
        1,
        50,
        {
            "expand": "fk_id_copia.fk_id_libro.fk_id_genero"
        }
    )

    genero_lista = []
    for prestamo in prestamos.items:
        copia = prestamo.expand.get("fk_id_copia")
        if copia:
            libro = copia.expand.get("fk_id_libro")
            if libro:
                generos = libro.expand.get("fk_id_genero")
                if generos:
                    for genero in generos:
                        genero_lista.append(genero.genero)

    conteo_generos = Counter(genero_lista)
    conteos_mensuales = []
    for gnere, count in conteo_generos.items():
        print(gnere, count)
        obj_cont_mensual = { "nombre": gnere, "cantidad": count }
        conteos_mensuales.append(obj_cont_mensual)

    return conteos_mensuales


def db_get_prestamos_por_mes(pk_id_usuario: int) -> Dict:
    client = db_get_client()
    usuario = db_get_usuario(pk_id_usuario)
    prestamos = client.collection("Prestamos").get_list(
        1,
        20,
        {
            "filter": f'fk_id_usuario = "{usuario.id}"'
        }
    )
    months = [datetime.fromisoformat(r.created_at.replace("Z", "+00:00")).strftime("%Y-%m") for r in  prestamos.items]
    conteo_por_mes = Counter(months)
    return conteo_por_mes

def db_get_prestamos_por_mes_admin() -> List:
    client = db_get_client()
    prestamos = client.collection("Prestamos").get_list(
        1,
        20
    )
    months = [datetime.fromisoformat(r.created_at.replace("Z", "+00:00")).strftime("%B") for r in  prestamos.items]
    conteo_por_mes = Counter(months)
    print(conteo_por_mes)
    conteos_mensuales = []
    for month, count in conteo_por_mes.items():
        print(month, count)
        conteos_mensuales = []
        obj_cont_mensual = { "mes": month, "prestamos": count }
        conteos_mensuales.append(obj_cont_mensual)

    return conteos_mensuales

def db_delete_prestamo(pk_id_prestamo: int) -> Response:
    client = db_get_client()
    prestamo = client.collection("Prestamos").get_first_list_item(
        f'pk_id_prestamo = {pk_id_prestamo}'
    )
    return client.collection("Prestamos").delete(prestamo.id)

from collections import Counter
from datetime import datetime
from typing import Dict, List, Tuple

from requests.models import Response

from app.interfaces.ml import get_ml_recomendaciones
from app.core.auth import db_get_client
from app.models.db_models import Prestamo
from app.pb_clients.usuarios import db_get_usuario

from app.pb_clients.libros import *

import time

from app.core.config import settings

LIBROS_CACHE: List
CACHE_LAST_UPDATE = 0
CACHE_TTL = 60  # segundos (ej: 1 minuto)

def db_get_last_id_prestamo() -> int:
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

def db_create_prestamo(prestamo: Prestamo) -> Prestamo:
    client = db_get_client()
    last_prestamo = db_get_last_id_prestamo()
    
    record = client.collection("Prestamos").create(
            {
                "pk_id_prestamo":  last_prestamo + 1, # genero.pk_id_genero, antes de actualizacion
                "fk_id_copia": prestamo.fk_id_copia,
                "fk_id_usuario": prestamo.fk_id_usuario,
                "fecha_prestamo": prestamo.fecha_prestamo,
                "fecha_entrega": prestamo.fecha_entrega,
                "dias_restantes": prestamo.dias_restantes,
                "estatus_entrega": prestamo.estatus_entrega
            },
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

def db_get_historial_prestamos(fk_id_usuario: str, limit: int) -> List:
    client = db_get_client()
    
    # En get_list(page, per_page, options):
    # Usamos page=1 y per_page=limit para obtener exactamente la cantidad deseada.
    prestamos = client.collection("Prestamos").get_list(
        1,
        limit,
        {
            "filter": f'fk_id_usuario = "{fk_id_usuario}"',
            "expand": "fk_id_copia.fk_id_libro.fk_id_genero",
            "sort": "-created_at"  # Trae los más nuevos primero
        }
    )
    
    mis_prestamos = []

    for prestamo in prestamos.items:
        titulo_libro = "Sin título"
        autor = "Desconocido"
        genero_lista = []
        
        # Acceso seguro a los niveles de expansión
        expand_prestamo = getattr(prestamo, "expand", {})
        copia = expand_prestamo.get("fk_id_copia")
        
        if copia:
            expand_copia = getattr(copia, "expand", {})
            libro = expand_copia.get("fk_id_libro")
            
            if libro:
                titulo_libro = getattr(libro, "titulo", titulo_libro)
                autor = getattr(libro, "autor", autor)
                
                expand_libro = getattr(libro, "expand", {})
                generos = expand_libro.get("fk_id_genero")
                
                if generos:
                    # Manejo si generos es una lista (relación múltiple)
                    if isinstance(generos, list):
                        genero_lista = [getattr(g, "genero", "") for g in generos]
                    else:
                        genero_lista = [getattr(generos, "genero", "")]

        libros_prestados = {
            "id": getattr(prestamo, "pk_id_prestamo", prestamo.id),
            "titulo": titulo_libro,
            "autor": autor,
            "genero": genero_lista,
            "fecha_prestamo": getattr(prestamo, "fecha_prestamo", ""),
            "fecha_devolucion": getattr(prestamo, "fecha_entrega", ""),
            "estatus_entrega": "En préstamo" if not getattr(prestamo, "estatus_entrega", False) else "Devuelto",
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
        estrellas = 0
        genero_lista = []
        copia = prestamo.expand.get("fk_id_copia")
        if copia:
            libro = copia.expand.get("fk_id_libro")
            if libro:
                titulo_libro = libro.titulo
                autor = libro.autor
                descripcion = libro.descripcion
                estrellas = libro.estrellas
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
            "estrellas": estrellas,
            "fecha_prestamo": prestamo.fecha_prestamo,
            "fecha_entrega": prestamo.fecha_entrega,
            "estatus_entrega": prestamo.estatus_entrega,
        }
        mis_prestamos.append(libros_prestados)
    recomendaciones = get_ml_recomendaciones(mis_prestamos)

    return recomendaciones


def db_get_total_prestamos() -> int:
    client = db_get_client()
    result = client.collection("Prestamos").get_list(1, 1)
    total_count = result.total_items
    print("Total Prestamos:", total_count)

    return total_count

def db_get_total_mis_prestamos(fk_id_usuario: str) -> Dict:
    client = db_get_client()
    
    # Aplicamos el filtro para que el conteo sea solo de ese usuario
    # El filtro usa sintaxis de PocketBase: "campo = 'valor'"
    result = client.collection("Prestamos").get_list(1, 1, {
        "filter": f'fk_id_usuario = "{fk_id_usuario}"'
    })
    
    total_count = result.total_items
    print(f"Total Prestamos para el usuario {fk_id_usuario}: {total_count}")

    return {"total": total_count}


def db_get_historial_paginado(offset: int, limit: int) -> Tuple[List[Dict], int]:
    """
    Retorna el historial de préstamos de manera paginada.
    Retorna una tupla: (lista_de_prestamos, total_de_items_en_db)
    """
    client = db_get_client()
    page = (offset // limit) + 1
    
    # PocketBase get_list(page, perPage, options)
    # page: El número de página (empieza en 1)
    # per_page: Cuántos registros traer
    response = client.collection("Prestamos").get_list(
        page,
        limit,
        {
            "expand": "fk_id_copia.fk_id_libro.fk_id_genero, fk_id_usuario",
            "sort": "-created_at" 
        }
    )
    
    mis_prestamos = []
    print(response.items)
    for prestamo in response.items:
        
        titulo_libro = "Desconocido"
        autor = "Desconocido"
        nombre_usuario = "Desconocido"
        correo_usuario = "Desconocido"
        id_usuario = "Desconocido"
        genero_lista = []
        
        # Navegación segura por los niveles de expand
        expand_p = getattr(prestamo, "expand", {})
        copia = expand_p.get("fk_id_copia")
        usuario = expand_p.get("fk_id_usuario")
        
        if usuario:
            nombre_usuario = usuario.nombre_usuario
            correo_usuario = usuario.email
            id_usuario = usuario.pk_id_usuario

        if copia:
            expand_c = getattr(copia, "expand", {})
            libro = expand_c.get("fk_id_libro")
            
            if libro:
                titulo_libro = getattr(libro, "titulo", "")
                autor = getattr(libro, "autor", "")
                
                expand_l = getattr(libro, "expand", {})
                generos = expand_l.get("fk_id_genero")
                
                if generos:
                    # PocketBase devuelve una lista si es relación múltiple o un objeto si es única
                    if isinstance(generos, list):
                        genero_lista = [g.get("genero") if isinstance(g, dict) else getattr(g, "genero", "") for g in generos]
                    else:
                        genero_lista = [getattr(generos, "genero", "")]

        libros_prestados = {
            "usuario": nombre_usuario,
            "email": correo_usuario,
            "id_usuario": id_usuario,
            "pk_id_prestamo": prestamo.id, # O prestamo.pk_id_prestamo si es un campo manual
            "titulo": titulo_libro,
            "autor": autor,
            "genero": genero_lista,
            "fecha_prestamo": getattr(prestamo, "fecha_prestamo", ""),
            "fecha_entrega": getattr(prestamo, "fecha_entrega", ""),
            "estatus_entrega": getattr(prestamo, "estatus_entrega", False),
            "isbn": copia.isbn,
            "rfid_tag": copia.rfid_tag
        }
        mis_prestamos.append(libros_prestados)
    
    # Retornamos los datos procesados y el total de registros (totalItems)
    return mis_prestamos, response.total_items

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

def db_get_generos_leidos_usuario(fk_id_usuario: str) -> List:
    client = db_get_client()
    prestamos = client.collection("Prestamos").get_list(
        1,
        50,
        {
            "expand": "fk_id_copia.fk_id_libro.fk_id_genero",
            "filter": f'fk_id_usuario = "{fk_id_usuario}"'
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
        obj_cont_mensual = { "genero": gnere, "total": count }
        conteos_mensuales.append(obj_cont_mensual)

    return conteos_mensuales



def db_get_prestamos_por_mes(pk_id_usuario: str) -> Dict:
    client = db_get_client()
    prestamos = client.collection("Prestamos").get_list(
        1,
        20,
        {
            "filter": f'fk_id_usuario = "{pk_id_usuario}"'
        }
    )
    months = [datetime.fromisoformat(r.created_at.replace("Z", "+00:00")).strftime("%B") for r in  prestamos.items]
    conteo_por_mes = Counter(months)
    conteos_mensuales = []
    for month, count in conteo_por_mes.items():
        print(month, count)
        conteos_mensuales = []
        obj_cont_mensual = { "mes": month, "prestamos": count }
        conteos_mensuales.append(obj_cont_mensual)

    return conteos_mensuales

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

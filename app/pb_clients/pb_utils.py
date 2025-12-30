from typing import List
from collections import Counter

from app.core.auth import db_get_client


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

    base_url = "http://localhost:8090"
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


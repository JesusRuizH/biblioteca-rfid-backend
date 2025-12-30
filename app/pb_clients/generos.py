import os
from typing import List
from requests.models import Response
from app.models.db_models import Generos

from app.models.queries_models import GenerosQuery
from app.core.auth import db_get_client

from pocketbase.client import FileUpload


def db_create_genero(genero: Generos) -> Generos:
    client = db_get_client()
    direccion_img = genero.icon

    filename = os.path.basename(direccion_img)
    with open(direccion_img, "rb") as f:
        file_upload = FileUpload(filename, f)
        genero_record = client.collection("Generos").create(
            {
                "pk_id_genero": genero.pk_id_genero,
                "genero": genero.genero,
                "created_at": genero.created_at,
                "updated_at": genero.updated_at,
                "icon": file_upload
            },
        )

    return Generos(
        id=genero_record.id,
        pk_id_genero=genero_record.pk_id_genero,
        genero=genero_record.genero,
        icon=genero_record.icon,
        created_at=genero_record.created_at,
        updated_at=genero_record.updated_at
    )


def db_get_genero(pk_id_genero: int) -> Generos:
    client = db_get_client()
    genero_record = client.collection("Generos").get_first_list_item(
        f'pk_id_genero = "{pk_id_genero}"'
    )
    return Generos(
        id=genero_record.id,
        pk_id_genero=genero_record.pk_id_genero,
        genero=genero_record.genero,
        icon=genero_record.icon,
        created_at=genero_record.created_at,
        updated_at=genero_record.updated_at
    )


def db_get_all_generos() -> List[Generos]:
    client = db_get_client()
    base_url = "http://localhost:8090"
    collection_id = "pbc_2202816583"
    generos_records = client.collection("Generos").get_full_list()
    generos_list = []
    for g in generos_records:
        generos_list.append(
            Generos(
                id=g.id,
                pk_id_genero=g.pk_id_genero,
                genero=g.genero,
                icon=f"{base_url}/api/files/{collection_id}/{g.id}/{g.icon}",
                created_at=g.created_at,
                updated_at=g.updated_at
            )
        )
    return generos_list


def db_update_genero(genero: Generos) -> Generos:
    client = db_get_client()
    genero_actual = db_get_genero(genero.pk_id_genero)

    if genero_actual.icon != genero.icon:
        direccion_img = genero.icon
        filename = os.path.basename(direccion_img)
        with open(direccion_img, "rb") as f:
            file_upload = FileUpload(filename, f)
            record = (client.collection("Generos").
                      update(genero.id,
                             {
                                "pk_id_genero": genero.pk_id_genero,
                                 "genero": genero.genero,
                                 "icon": file_upload,
                                 "created_at": genero.created_at,
                                 "updated_at": genero.updated_at,
                             }
                            )
                      )
    else:
        record = client.collection("Generos").update(
            genero.id, genero.model_dump(mode="json")
        )
    return Generos(
        id=record.id,
        pk_id_genero=record.pk_id_genero,
        genero=record.genero,
        icon=record.icon,
        created_at=record.created_at,
        updated_at=record.updated_at
    )


def db_delete_genero(pk_id_genero: int) -> Response:
    client = db_get_client()
    genero_record = client.collection("Generos").get_first_list_item(
        f'pk_id_genero = "{pk_id_genero}"'
    )
    response = client.collection("Generos").delete(genero_record.id)
    return response

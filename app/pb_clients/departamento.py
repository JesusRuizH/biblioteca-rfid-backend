from typing import List

from requests.models import Response
from app.models.db_models import Departamento
from app.core.auth import db_get_client

#id: str
#pk_id_departamento: int
#numero: int
#nombre: str
#created_at: Optional[date]
#updated_at: Optional[date]

def db_create_departamento(departamento: Departamento):
    client = db_get_client()
    departamento = client.collection("Departamentos").create(departamento.model_dump(mode="json"))
    return Departamento(
        id=departamento.id,
        pk_id_departamento=departamento.pk_id_departamento,
        numero=departamento.numero,
        nombre=departamento.nombre,
        created_at=departamento.created_at,
        updated_at=departamento.updated_at
    )

def db_get_departamento(pk_id_departamento: int) -> Departamento:
    client = db_get_client()
    departamento = client.collection("Departamentos").get_first_list_item(
        f'pk_id_departamento = "{pk_id_departamento}"'
    )
    return Departamento(
        id=departamento.id,
        pk_id_departamento=departamento.pk_id_departamento,
        numero=departamento.numero,
        nombre=departamento.nombre,
        created_at=departamento.created_at,
        updated_at=departamento.updated_at
    )

def db_get_all_dptos() -> List[Departamento]:
    client = db_get_client()
    record = client.collection("Departamentos").get_full_list()
    dpto_list = []
    for r in record:
        dpto_list.append(
             Departamento(
                 id=r.id,
                 pk_id_departamento=r.pk_id_departamento,
                 numero=r.numero,
                 nombre=r.nombre,
                 created_at=r.created_at,
                 updated_at=r.updated_at
            )
        )
    return dpto_list

def db_update_departamento(departamento:Departamento) -> Departamento:
    client = db_get_client()
    departamento = client.collection("Departamentos").update(departamento.id,
                                                               departamento.model_dump(mode="json"))
    return Departamento(
        id=departamento.id,
        pk_id_departamento=departamento.pk_id_departamento,
        numero=departamento.numero,
        nombre=departamento.nombre,
        created_at=departamento.created_at,
        updated_at=departamento.updated_at
    )

def db_delete_departamento(pk_id_departamento :int) -> Response:
    client = db_get_client()
    departamento = client.collection("Departamentos").get_first_list_item(
        f"pk_id_departamento = {pk_id_departamento}"
    )
    response = client.collection("Departamentos").delete(departamento.id)
    return response
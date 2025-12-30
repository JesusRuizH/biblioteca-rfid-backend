from typing import List

from app.core.auth import db_get_client
from app.models.db_models import TipoUsuario
from requests.models import Response

def db_create_tipo_usuario(tipo_usuario: TipoUsuario) -> TipoUsuario:
    client = db_get_client()
    record = client.collection("TipoUsuario").create(tipo_usuario.model_dump(mode="json"))
    return TipoUsuario(
        id=record.id,
        pk_id_tipo_usuario=record.pk_id_tipo_usuario,
        rol=record.rol,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


def db_get_tipo_usuario(pk_id_tipo_usuario: int) -> TipoUsuario:
    client = db_get_client()
    record = client.collection("TipoUsuario").get_first_list_item(
        f'pk_id_tipo_usuario = {pk_id_tipo_usuario}'
    )
    return TipoUsuario(
        id=record.id,
        pk_id_tipo_usuario=record.pk_id_tipo_usuario,
        rol=record.rol,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


def db_get_all_tipo_usuario() -> List[TipoUsuario]:
    client = db_get_client()
    record = client.collection("TipoUsuario").get_full_list()
    tipos_list = []
    for r in record:
        tipos_list.append(
         TipoUsuario(
            id=r.id,
            pk_id_tipo_usuario=r.pk_id_tipo_usuario,
            rol=r.rol,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
    )
    return tipos_list

def db_update_tipo_usuario(tipo_usuario: TipoUsuario) -> TipoUsuario:
    client = db_get_client()
    updated = client.collection("TipoUsuario").update(
        tipo_usuario.id, tipo_usuario.model_dump(mode="json")
    )
    return TipoUsuario(
        id=updated.id,
        pk_id_tipo_usuario=updated.pk_id_tipo_usuario,
        rol=updated.rol,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
    )


def db_delete_tipo_usuario(pk_id_tipo_usuario: int) -> Response:
    client = db_get_client()

    tipo_usuario = client.collection("TipoUsuario").get_first_list_item(
        f'pk_id_tipo_usuario = "{pk_id_tipo_usuario}"'
    )

    return client.collection("TipoUsuario").delete(tipo_usuario.id)

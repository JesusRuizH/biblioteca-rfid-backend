from datetime import date, datetime
from typing import List, Dict
from pocketbase import PocketBase
from app.core.config import settings

from requests.models import Response
from app.core.auth import db_get_client
from app.models.db_models import Usuario
from app.models.queries_models import EstadisticasAdminPanelA, MetricasValores, TopLibrosAdminPanel, MetricasAdminPanel
from app.pb_clients.pb_utils import db_get_top_libros

from datetime import datetime, timedelta
from collections import Counter


def db_create_usuario(usuario: Usuario) -> Usuario:
    client = db_get_client()
    record = client.collection("Usuarios").create(usuario.model_dump(mode="json"))
    return Usuario(
        id=record.id,
        pk_id_usuario=record.pk_id_usuario,
        nombre_usuario=record.nombre_usuario,
        email=record.email.lower(),
        verified=record.verified,
        fk_id_tipo_usuario=record.fk_id_tipo_usuario,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )

def db_get_all_usuarios() -> List[Usuario]:
    client = db_get_client()
    record = client.collection("Usuarios").get_full_list()
    usuarios_list = []
    for r in record:
        usuarios_list.append(
             Usuario(
                id=r.id,
                pk_id_usuario=r.pk_id_usuario,
                nombre_usuario=r.nombre_usuario,
                email=r.email,
                verified=r.verified,
                fk_id_tipo_usuario=r.fk_id_tipo_usuario,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
        )
    return usuarios_list


def db_get_usuario(pk_id_usuario: int) -> Usuario:
    client = db_get_client()
    record = client.collection("Usuarios").get_first_list_item(
        f'pk_id_usuario = {pk_id_usuario}'
    )
    return Usuario(
        id=record.id,
        pk_id_usuario=record.pk_id_usuario,
        nombre_usuario=record.nombre_usuario,
        email=record.email,
        verified=record.verified,
        fk_id_tipo_usuario=record.fk_id_tipo_usuario,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )

def db_auth_usuario(email: str, password: str) -> Usuario:
    client = PocketBase(f'{settings.POCKETBASE_URL}')
    auth_data = client.collection("Usuarios").auth_with_password(email.lower(), password)
    record = auth_data.record
    id_tipo_usuario = str(record.fk_id_tipo_usuario)
    rol = ""
    tipo_usuario = client.collection("TipoUsuario").get_one(id_tipo_usuario)
    if tipo_usuario is None:
        rol = "NA"
    else:
        rol = tipo_usuario.rol

    return Usuario(
        id=record.id,
        pk_id_usuario=record.pk_id_usuario,
        nombre_usuario=record.nombre_usuario,
        email=record.email,
        verified=record.verified,
        fk_id_tipo_usuario= rol,
        fecha_nacimiento=record.fecha_nacimiento,
        created_at=record.created,
        updated_at=record.updated,
    )

def db_auth_admin(email: str, password: str) -> Usuario:
    client = PocketBase(f'{settings.POCKETBASE_URL}')

    # autenticamos con email + password
    auth_data = client.collection("Usuarios").auth_with_password(email.lower(), password)
    record = auth_data.record

    # validar que sea admin (campo fk_id_tipo_usuario)
    if record.fk_id_tipo_usuario != "u1l39l9q865oq3v":
        raise PermissionError("El usuario no tiene privilegios de administrador")

    return Usuario(
        id=record.id,
        pk_id_usuario=record.pk_id_usuario,
        nombre_usuario=record.nombre_usuario,
        email=record.email,
        verified=record.verified,
        fk_id_tipo_usuario=record.fk_id_tipo_usuario,
        fecha_nacimiento=record.fecha_nacimiento,
        created_at=record.created,
        updated_at=record.updated,
    )

def db_get_last_id_usuario() -> int:
    client = db_get_client()
    last_user = client.collection("Usuarios").get_list(
        page=1,
        per_page=1,
        query_params={
            "sort": "-pk_id_usuario"
        }
    )
    if not last_user.items:
        return 0
    return last_user.items[0].pk_id_usuario

def db_update_usuario(usuario: Usuario) -> Usuario:
    client = db_get_client()
    updated = client.collection("Usuarios").update(
        usuario.id, usuario.model_dump(mode="json")
    )
    return Usuario(
        id=updated.id,
        pk_id_usuario=updated.pk_id_usuario,
        nombre_usuario=updated.nombre_usuario,
        email=updated.email,
        verified=updated.verified,
        fk_id_tipo_usuario=updated.fk_id_tipo_usuario,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
    )


def db_delete_usuario(pk_id_usuario: int) -> Response:
    client = db_get_client()
    usuario = client.collection("Usuarios").get_first_list_item(
        f'pk_id_usuario = {pk_id_usuario}'
    )
    return client.collection("Usuarios").delete(usuario.id)


def db_get_historial_libros(pk_id_usuario) -> List:
    client = db_get_client()
    user = db_get_usuario(pk_id_usuario)
    historial_libros = client.collection("Prestamos").get_full_list(
        query_params={"filter": f'fk_id_usuario = "{user.id}"'}
    )
    return historial_libros


def db_get_estadisticas_admin_panel_a() -> EstadisticasAdminPanelA:

    metricas = get_metrics()
    top = top_libros()
    ultimos_siete_dias = get_prestamos_ultimos_siete_dias()
    conteo_ultimos_siete_dias = []
    for dia, prestamos in ultimos_siete_dias.items():
        conteo_ultimos_siete_dias.append(prestamos)

    estadisticas_admin_panel = EstadisticasAdminPanelA(
        Metricas=metricas,
        TopLibros=top,
        SeriePrestamos=conteo_ultimos_siete_dias
    )

    return estadisticas_admin_panel


def top_libros() -> List:
    top_libros_ = db_get_top_libros(5)
    top_libros_lista = []
    for libro in top_libros_:
        top_libros_lista.append(TopLibrosAdminPanel(titulo=libro["titulo"], prestamos=libro["veces_prestado"]))
    return top_libros_lista

def get_metrics() -> MetricasAdminPanel:
    client = db_get_client()

    # get today date boundaries in ISO format with milliseconds
    today = date.today()
    start = datetime.combine(today, datetime.min.time()).isoformat(timespec="milliseconds") + "Z"
    end = datetime.combine(today, datetime.max.time()).isoformat(timespec="milliseconds") + "Z"

    # Usuarios
    result_clientes = client.collection("Usuarios").get_list(1, 1)
    total_count_usuarios = result_clientes.total_items

    # Prestamos (really Libros today)
    result_prestamos = client.collection("Libros").get_list(
        1,
        50,
        {"filter": f'created_at >= "{start}" && created_at <= "{end}"'}
    )
    total_count_prestamos = result_prestamos.total_items

    # Libros total
    result_libros = client.collection("Libros").get_list(1, 1)
    total_count_libros = result_libros.total_items

    metrics_usuarios = MetricasValores(Total=total_count_usuarios, Delta="+12 este mes", Up=True)
    metrics_libros = MetricasValores(Total=total_count_libros, Delta="+7 este mes", Up=True)
    metrics_prestamos = MetricasValores(Total=total_count_prestamos, Delta="+3 este mes", Up=False)

    return MetricasAdminPanel(
        Usuarios=metrics_usuarios,
        Libros=metrics_libros,
        PrestamosHoy=metrics_prestamos,
    )

def get_prestamos_ultimos_siete_dias() -> Dict:
    client = db_get_client()
    # Obtener la fecha de hace 7 días
    hoy = datetime.utcnow().date()
    hace_7 = hoy - timedelta(days=6)

    # El filtro correcto para PocketBase:
    filter_query = f'created_at >= "{hace_7.isoformat()}T00:00:00Z"'

    registros = client.collection("Prestamos").get_full_list(
        query_params={"filter": filter_query}
    )

    conteo_por_dia = Counter()
    for r in registros:
        fecha = datetime.fromisoformat(r.created_at).date()
        conteo_por_dia[str(fecha)] += 1

    resultado = {}
    for i in range(7):
        dia = hace_7 + timedelta(days=i)
        resultado[str(dia)] = conteo_por_dia.get(str(dia), 0)

    return resultado
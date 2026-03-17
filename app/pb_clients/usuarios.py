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


def db_get_last_id_usuario() -> int:
    client = db_get_client()
    last_usuario = client.collection("Usuarios").get_list(
        page=1,
        per_page=1,
        query_params={
            "sort": "-pk_id_usuario"
        }
    )
    if not last_usuario.items:
        return 0
    return last_usuario.items[0].pk_id_usuario

def db_create_usuario(usuario: Usuario) -> Usuario:
    client = db_get_client()
    last_usuario = db_get_last_id_usuario()

    record = client.collection("Usuarios").create({
            "pk_id_usuario": last_usuario + 1,
            "nombre_usuario": usuario.nombre_usuario.title(),
            "password": usuario.password,
            "passwordConfirm":usuario.passwordConfirm,
            "email": usuario.email.lower(),
            "verified": usuario.verified,
            "fk_id_tipo_usuario": usuario.fk_id_tipo_usuario
        })
    
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

def db_get_users_paginados(limit: int, offset: int, q = None) -> Dict:
    client = db_get_client()

    page = (offset // limit) + 1

    query_params = {
        "expand": "fk_id_libro"
    }

    if q:
        q = q.strip()
        query_params["filter"] = f'email ~ "{q}" || nombre_usuario ~ "{q}"'

    record = client.collection("Usuarios").get_list(
        page,
        limit,
        query_params=query_params)
    
    usuarios_list = []
    for r in record.items:
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

    response = {
        "items": usuarios_list,
        "total": record.total_items
    }
    return response


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
        created_at=record.created_at,
        updated_at=record.updated_at,
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

    ahora_local = datetime.now()
    medianoche_hoy_local = ahora_local.replace(hour=0, minute=0, second=0, microsecond=0)

  
    desfase = timedelta(hours=8)
    
    filtro_hoy_inicio = (medianoche_hoy_local - desfase).strftime("%Y-%m-%d %H:%M:%S")

    # --- PRÉSTAMOS HOY ---
    res_hoy = client.collection("Prestamos").get_list(1, 1, {
        "filter": f'created_at >= "{filtro_hoy_inicio}"'
    })
    prestamos_hoy = res_hoy.total_items

    # --- SERIE DE LA SEMANA ---
    serie_prestamos = []
    for i in range(6, -1, -1):
        inicio_dia_utc = medianoche_hoy_local - timedelta(days=i) + desfase
        fin_dia_utc = inicio_dia_utc + timedelta(days=1)
        
        q_start = inicio_dia_utc.strftime("%Y-%m-%d %H:%M:%S")
        q_end = fin_dia_utc.strftime("%Y-%m-%d %H:%M:%S")
        
        count = client.collection("Prestamos").get_list(1, 1, {
            "filter": f'created_at >= "{q_start}" && created_at < "{q_end}"'
        }).total_items
        serie_prestamos.append(count)

    # --- RESTO DE MÉTRICAS ---
    filtro_mes = (medianoche_hoy_local - timedelta(days=30) + desfase).strftime("%Y-%m-%d %H:%M:%S")

    total_usuarios = client.collection("Usuarios").get_list(1, 1).total_items
    nuevos_usuarios = client.collection("Usuarios").get_list(1, 1, {
        "filter": f'created_at >= "{filtro_mes}"'
    }).total_items

    total_libros = client.collection("Libros").get_list(1, 1).total_items
    nuevos_libros = client.collection("Libros").get_list(1, 1, {
        "filter": f'created_at >= "{filtro_mes}"'
    }).total_items

    prestamos_mes = client.collection("Prestamos").get_list(1, 1, {
        "filter": f'created_at >= "{filtro_mes}"'
    }).total_items

    return MetricasAdminPanel(
        Usuarios=MetricasValores(Total=total_usuarios, Delta=f"+{nuevos_usuarios} este mes", Up=nuevos_usuarios > 0),
        Libros=MetricasValores(Total=total_libros, Delta=f"+{nuevos_libros} este mes", Up=nuevos_libros > 0),
        PrestamosHoy=MetricasValores(Total=prestamos_hoy, Delta=f"{prestamos_mes} en 30d", Up=prestamos_hoy > 0),
        SeriePrestamos=serie_prestamos
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
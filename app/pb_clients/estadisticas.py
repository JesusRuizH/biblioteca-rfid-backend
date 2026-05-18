from typing import Dict, List
from app.core.auth import db_get_client
from app.pb_clients.prestamos import get_libros_cache
from zoneinfo import ZoneInfo
from collections import Counter
from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone


def db_get_statistics() -> Dict:
    client = db_get_client()
    
    # 1. Resúmenes rápidos (Asegúrate que los nombres de las colecciones sean exactos)
    res_libros = client.collection("Libros").get_list(1, 1)
    res_usuarios = client.collection("Usuarios").get_list(1, 1)
    res_prestamos = client.collection("Prestamos").get_list(1, 1)

    # 2. Préstamos por día (Optimizado en una sola petición)
    prestamosPorDia = get_last_14_days_statistics(client)

    # 3. Inventario (CORRECCIÓN DE FILTRO)
    # Si 'disponibilidad' está en 'Libros', cámbialo a la colección 'Libros'
    # Si es un campo de 'Prestamos', asegúrate que exista en el admin panel.
    try:
        libros_disponibles = client.collection("CopiasLibro").get_list(
            1, 1, query_params={"filter": "disponibilidad=true"}
        )
        libros_prestados = client.collection("CopiasLibro").get_list(
            1, 1, query_params={"filter": "disponibilidad=false"}
        )
        disp_count = libros_disponibles.total_items
        prest_count = libros_prestados.total_items
    except Exception as e:
        print(f"Error en filtros de disponibilidad: {e}")
        disp_count, prest_count = 0, 0

    # 4. Top Libros
    libros = get_libros_cache()
    top = [{"titulo": l['titulo'], "prestamos": l['veces_prestado']} for l in libros]

    # 5. Usuarios Activos (Optimización sugerida abajo)
    usuariosActivos = top_10_users_manual(client)

    return {
        "resumen": {
            "usuarios": res_usuarios.total_items,
            "libros": res_libros.total_items,
            "prestamosTotal": res_prestamos.total_items
        },
        "prestamosPorDia": prestamosPorDia,
        "inventarioPorEstado": {
            "disponible": disp_count,
            "prestado": prest_count,
        },
        "topLibros": top,
        "usuariosActivos": usuariosActivos
    }

def get_last_14_days_statistics(client) -> List[Dict]:
    # 1. Define Mexico City and UTC timezones
    mx_tz = ZoneInfo("America/Mexico_City")
    utc_tz = ZoneInfo("UTC")

    # 2. Get current time in Mexico City and calculate local start date (13 days ago + today = 14 days)
    ahora_local = datetime.now(mx_tz)
    start_date_local = (ahora_local - timedelta(days=13)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 3. Convert local start date to UTC for the PocketBase filter boundary
    start_date_utc = start_date_local.astimezone(utc_tz)
    start_str = start_date_utc.strftime("%Y-%m-%d %H:%M:%S")

    records = client.collection("Prestamos").get_full_list(
        query_params={
            "filter": f'fecha_prestamo >= "{start_str}"',
            "fields": "fecha_prestamo"
        }
    )

    # 4. Extract dates localized to Mexico City before counting
    fechas_locales = []
    for r in records:
        if r.fecha_prestamo:
            # Standardize string Z to +00:00 and parse to aware UTC
            dt_str = r.fecha_prestamo.replace("Z", "+00:00")
            dt_utc = datetime.fromisoformat(dt_str)
            
            # Convert to Mexico City time to extract the true local calendar day
            dt_local = dt_utc.astimezone(mx_tz)
            fechas_locales.append(dt_local.strftime("%Y-%m-%d"))

    counts = Counter(fechas_locales)

    # 5. Build the 14-day sequence using Mexico City dates
    results = []
    for i in range(14):
        date_str = (start_date_local + timedelta(days=i)).strftime("%Y-%m-%d")
        results.append({
            "d": date_str, 
            "n": counts.get(date_str, 0)
        })
        
    return results


def top_10_users_manual(client):
    # 1️⃣ Obtener todos los préstamos
    prestamos = client.collection("Prestamos").get_full_list()

    if not prestamos:
        return []

    # 2️⃣ Contar repeticiones de fk_id_usuario
    counter = Counter(p.fk_id_usuario for p in prestamos)

    # 3️⃣ Obtener los 10 con más préstamos
    top_10 = counter.most_common(10)

    result = []

    for user_id, count in top_10:
        try:
            user = client.collection("Usuarios").get_one(user_id)

            result.append({
                "nombre": user.nombre_usuario,  # o user.name si lo tienes
                "prestamos": count
            })

        except Exception:
            # Si el usuario fue eliminado o hay error
            result.append({
                "nombre": f"Usuario eliminado ({user_id})",
                "prestamos": count
            })

    return result

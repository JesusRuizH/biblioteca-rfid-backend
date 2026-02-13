from typing import Dict
from app.core.auth import db_get_client
from app.pb_clients.prestamos import get_libros_cache
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

def get_last_14_days_statistics(client):
    today = datetime.now(timezone.utc)
    start_date = (today - timedelta(days=13)).replace(hour=0, minute=0, second=0, microsecond=0)
    # PocketBase acepta 'YYYY-MM-DD HH:MM:SS' directamente en el filtro
    start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")

    records = client.collection("Prestamos").get_full_list(
        query_params={
            "filter": f'fecha_prestamo >= "{start_str}"',
            "fields": "fecha_prestamo"
        }
    )

    # Extraer fechas y contar
    counts = Counter(r.fecha_prestamo[:10] for r in records if r.fecha_prestamo)

    results = []
    for i in range(14):
        date_str = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        results.append({"d": date_str, "n": counts.get(date_str, 0)})
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

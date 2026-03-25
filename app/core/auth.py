from pocketbase import PocketBase
from app.core.config import settings

CLIENT = None

def db_get_client():
    global CLIENT
    
    if CLIENT is None:
        CLIENT = PocketBase(settings.POCKETBASE_URL)

    if not CLIENT.auth_store.token:
        CLIENT.admins.auth_with_password(settings.POCKETBASE_EMAIL, settings.POCKETBASE_PASSWORD)
    else:
        try:
            CLIENT.admins.auth_refresh()
        except Exception:
            # Si falla el refresh (token expirado o inválido), re-autenticamos
            try:
                CLIENT.admins.auth_with_password(settings.POCKETBASE_EMAIL, settings.POCKETBASE_PASSWORD)
            except Exception as e:
                print(f"Error crítico: No se pudo autenticar con PocketBase: {e}")
                return None

    return CLIENT
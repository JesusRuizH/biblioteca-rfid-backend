from pocketbase import PocketBase
from app.core.config import settings

CLIENT = None

def db_get_client():
    global CLIENT
    
    if CLIENT is None:
        CLIENT = PocketBase(settings.POCKETBASE_URL)

    # Use the new '_superusers' collection reference
    super_user_service = CLIENT.collection("_superusers")

    if not CLIENT.auth_store.token:
        try:
            # Login via the superusers collection
            super_user_service.auth_with_password(
                settings.POCKETBASE_EMAIL, 
                settings.POCKETBASE_PASSWORD
            )
        except Exception as e:
            print(f"Error crítico: Autenticación inicial fallida: {e}")
            return None
    else:
        try:
            # Refresh via the superusers collection
            super_user_service.auth_refresh()
        except Exception:
            try:
                # Re-auth if refresh fails
                super_user_service.auth_with_password(
                    settings.POCKETBASE_EMAIL, 
                    settings.POCKETBASE_PASSWORD
                )
            except Exception as e:
                print(f"Error crítico: No se pudo re-autenticar con PocketBase: {e}")
                return None

    return CLIENT
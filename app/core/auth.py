from pocketbase import PocketBase
from app.core.config import settings
# url = f"{URL}/api/collections/_superusers/auth-with-password"
CLIENT = None

def db_get_client():
    global CLIENT
    if not CLIENT:
        CLIENT = PocketBase(f'{settings.POCKETBASE_URL}')
        admin_data = CLIENT.admins.auth_with_password(f'{settings.POCKETBASE_EMAIL}', f'{settings.POCKETBASE_PASSWORD}')
        assert admin_data
    return CLIENT
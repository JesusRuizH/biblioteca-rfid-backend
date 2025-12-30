# app/core/auth.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("POCKETBASE_URL")
_identity = os.getenv("POCKETBASE_EMAIL")
_password = os.getenv("POCKETBASE_PASSWORD")

_token = None

def get_token() -> str:
    global _token
    if _token is None:
        _token = fetch_token()
    return _token

def fetch_token() -> str:
    url = f"{URL}/api/collections/_superusers/auth-with-password"
    data = {
        "identity": _identity,
        "password": _password
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code in (200, 201):
        print("✅ Token obtenido")
        return response.json()["token"]
    else:
        print("❌ Error al obtener token:", response.status_code, response.text)
        raise RuntimeError("Failed to authenticate")

def refresh_token():
    """Force-refresh the token (e.g. after logout, timeout)."""
    global _token
    _token = fetch_token()

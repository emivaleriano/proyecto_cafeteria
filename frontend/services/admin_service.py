import requests

from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent / ".env")

API_BASE_URL = os.getenv("API_BASE_URL")
def login_admin(usuario, contrasenia):
    """
    Retorna (datos, None) si el login es exitoso.
    Retorna (None, mensaje_error) si algo falla.
    """
    try:
        res = requests.post(
            f"{API_BASE_URL}/admin/login",
            json={"usuario": usuario, "contrasenia": contrasenia},
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()

    if res.status_code == 200 and body.get("exito"):
        return body.get("datos", {}), None

    return None, body.get("mensaje", "Error al iniciar sesión.")

def obtener_dashboard(token):
    """
    Retorna (datos, None) si la request es exitosa.
    Retorna (None, mensaje_error) si algo falla.
    """
    headers = {'Authorization': f'Bearer {token}'}

    try:
        res = requests.get(
            f"{API_BASE_URL}/admin/dashboard",
            headers=headers,
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        return None, "No se puedo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()

    if res.status_code == 200 and body.get("exito"):
        return body.get("datos", {}), None

    return None, body.get("mensaje", "Error al obtener el dashboard")

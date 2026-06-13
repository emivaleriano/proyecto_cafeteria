import requests

from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent / ".env")

API_BASE_URL = os.getenv("API_BASE_URL")

def _headers(token):
    return {"Authorization": f"Bearer {token}"}

def _handle(res, codigo_exito, mensaje_default):
    """Parsea la respuesta y retorna (datos, None) o (None, error)."""
    if res.status_code == 401:
        body = res.json()
        return None, body.get("mensaje", "Token expirado")
    body = res.json()
    if res.status_code == codigo_exito and body.get("exito"):
        return body.get("datos", {}), None
    return None, body.get("mensaje", mensaje_default)

def _request(method, url, token=None, json=None):
    """ConnectionError y Timeout.
    Unifica el connection y timeout para evitar la repeticion en cada funcion"""
    try:
        return requests.request(
            method,
            url,
            headers=_headers(token) if token else {},
            json=json,
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None


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

def service_cambiar_contrasenia(contra_actual, nueva_contra, confirmar_contra, token):
    if nueva_contra != confirmar_contra:
        return None, "Las contraseñas no coinciden."

    if len(nueva_contra) < 8:
        return None, "La contraseña debe tener al menos 8 caracteres."

    res = _request(
        "PATCH",
        f"{API_BASE_URL}/admin/contrasenia",
        token=token,
        json={"contra_actual": contra_actual, "nueva_contra": nueva_contra}
    )

    if res is None:
        return None, "No se pudo conectar con el servidor."

    return _handle(res, 200, "Error al cambiar la contraseña.")


def cambiar_info_local(datos, token):
    res = _request("PUT", f"{API_BASE_URL}/admin/inicio/config", token=token, json=datos)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al editar la info del local.")

def obtener_info_local():
    res = _request("GET", f"{API_BASE_URL}/inicio")
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al obtener la configuracion.")


def obtener_franjas_horarias():
    res = _request("GET", f"{API_BASE_URL}/inicio/franjas")
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al obtener las franjas horarias.")


def cambiar_franjas_horarias(franjas, token):
    res = _request("PUT", f"{API_BASE_URL}/admin/inicio/franjas", token=token, json={"franjas": franjas})
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al editar las franjas horarias.")

def obtener_dashboard(token): #stats
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


def service_obtener_dashboard(token): #pantalla
    """
    Llama a reservas, menú y servicios.
    """
    reservas  = _request("GET", f"{API_BASE_URL}/reservas",  token=token)
    platos    = _request("GET", f"{API_BASE_URL}/menu",             token=token)
    servicios = _request("GET", f"{API_BASE_URL}/servicios/",       token=token)

    def extraer(res, default=[]):
        if res is None:
            return default
        body = res.json()
        if res.status_code == 200 and body.get("exito"):
            return body.get("datos", default)
        return default

    return extraer(reservas), extraer(platos), extraer(servicios)


# ----------- Platos
def service_obtener_plato(id, token):
    res = _request("GET", f"{API_BASE_URL}/admin/menu/{id}", token=token)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al obtener el plato.")

def service_crear_plato(datos, token):
    res = _request("POST", f"{API_BASE_URL}/admin/menu", token=token, json=datos)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    print("STATUS:", res.status_code)
    print("BODY:", res.json())
    return _handle(res, 201, "Error al crear el plato.")

def service_editar_plato(id, datos, token):
    res = _request("PUT", f"{API_BASE_URL}/admin/menu/{id}", token=token, json=datos)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al editar el plato.")


def service_eliminar_plato(id, token):
    res = _request("DELETE", f"{API_BASE_URL}/admin/menu/{id}", token=token)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    if res.status_code == 204:
        return {}, None
    return _handle(res, 200, "Error al eliminar el plato.")



# ------------ Servicios
def service_obtener_servicio(id, token):
    res = _request("GET", f"{API_BASE_URL}/servicios/{id}", token=token)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al obtener el servicio.")


def service_crear_servicio(datos, token):
    res = _request("POST", f"{API_BASE_URL}/servicios/", token=token, json=datos)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 201, "Error al crear el servicio.")

def service_editar_servicio(id, datos, token):
    res = _request("PUT", f"{API_BASE_URL}/servicios/{id}", token=token, json=datos)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al editar el servicio.")

def service_eliminar_servicio(id, token):
    res = _request("DELETE", f"{API_BASE_URL}/servicios/{id}", token=token)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    if res.status_code == 204:
        return {}, None
    return _handle(res, 200, "Error al eliminar el servicio.")

def service_cambiar_estado_servicio(id, token):
    res = _request("PATCH", f"{API_BASE_URL}/servicios/{id}", token=token)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al cambiar el estado del servicio.")

# ------------- Reservas
def service_obtener_reserva(id, token):
    res = _request("GET", f"{API_BASE_URL}/reservas/{id}", token=token)
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al obtener la reserva.")


def service_actualizar_reserva(id, estado, token):
    res = _request("POST", f"{API_BASE_URL}/reservas/{id}/estado",
                   token=token, json={"estado": estado})
    if res is None:
        return None, "No se pudo conectar con el servidor."
    return _handle(res, 200, "Error al actualizar la reserva.")

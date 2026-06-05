import requests

from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent / ".env")

API_BASE_URL = os.getenv("API_BASE_URL")
ALERGIAS_OPCIONES = [
    {"id": "gluten",       "nombre": "Gluten"},
    {"id": "lactosa",      "nombre": "Lactosa"},
    {"id": "mariscos",     "nombre": "Mariscos"},
    {"id": "frutos_secos", "nombre": "Frutos secos"},
    {"id": "huevo",        "nombre": "Huevo"},
    {"id": "soja",         "nombre": "Soja"},
]

def get_inicio():
    """
    Llama a GET /inicio.
    Retorna (datos, None) o (None, mensaje_error).
    """
    try:
        res = requests.get(f"{API_BASE_URL}/inicio", timeout=10)
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()

    if res.status_code == 200 and body.get("exito"):
        return body.get("datos", {}), None

    return None, body.get("mensaje", "Error al obtener la información del local.")


# menu

def get_menu():
    """
    Llama a GET /menu.
    Retorna (lista_productos, None) o (None, mensaje_error).
    """
    try:
        res = requests.get(f"{API_BASE_URL}/menu", timeout=10)
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()

    if res.status_code == 200 and body.get("exito"):
        return body.get("datos", []), None

    return None, body.get("mensaje", "Error al obtener el menú.")


# reviews

def get_reviews():
    """
    Llama a GET /reviews.
    Retorna (lista_reviews, None) o (None, mensaje_error).
    """
    try:
        res = requests.get(f"{API_BASE_URL}/reviews", timeout=10)
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()

    if res.status_code == 200 and body.get("exito"):
        return body.get("datos", []), None

    return None, body.get("mensaje", "Error al obtener las reseñas.")


def post_review(id_reserva, estrellas, comentario):
    """
    Llama a POST /reservas/<id_reserva>/review.
    Retorna (datos, None) o (None, mensaje_error).
    """
    try:
        res = requests.post(
            f"{API_BASE_URL}/reservas/{id_reserva}/review",
            json={"estrellas": estrellas, "comentario": comentario},
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()

    if res.status_code == 201 and body.get("exito"):
        return body.get("datos", {}), None

    return None, body.get("mensaje", "Error al crear la reseña.")



def get_datos_reserva():
    inicio, error = get_inicio()
    if error:
        return None, error

    try:
        res = requests.get(f"{API_BASE_URL}/servicios/activos", timeout=10)
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()
    if res.status_code != 200 or not body.get("exito"):
        return None, body.get("mensaje", "Error al obtener los servicios.")

    return {
        "horarios":              inicio.get("horarios", []),
        "servicios_disponibles": body.get("datos", []),
        "alergias_opciones":     ALERGIAS_OPCIONES,
    }, None


def post_reserva(form):
    fecha      = form.get("fecha", "").strip()
    horario    = form.get("horario", "").strip()
    fecha_hora = f"{fecha}T{horario}"

    payload = {
        "nombre":            form.get("nombre", "").strip(),
        "email":             form.get("email", "").strip(),
        "telefono":          form.get("telefono", "").strip(),
        "cantidad_personas": form.get("cantidad_personas"),
        "fecha_hora":        fecha_hora,
        "alergias":          form.getlist("alergias[]"),
        "servicios":         form.getlist("servicios[]"),
        "observaciones":     form.get("comentarios", "").strip(),
    }

    try:
        res = requests.post(f"{API_BASE_URL}/reservas", json=payload, timeout=10)
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()
    if res.status_code == 201 and body.get("exito"):
        return body.get("datos", {}), None
    return None, body.get("mensaje", "Error al crear la reserva.")

def get_reserva(id_reserva):
    try:
        res = requests.get(f"{API_BASE_URL}/reservas/{id_reserva}", timeout=10)
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()
    if res.status_code == 200 and body.get("exito"):
        return body.get("datos", {}), None
    return None, body.get("mensaje", "Error al obtener la reserva.")


def post_cancelar_reserva(id_reserva):
    try:
        res = requests.patch(
            f"{API_BASE_URL}/reservas/{id_reserva}/cancelar",
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor."
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."

    body = res.json()
    if res.status_code == 200 and body.get("exito"):
        return body.get("datos", {}), None
    return None, body.get("mensaje", "Error al cancelar la reserva.")

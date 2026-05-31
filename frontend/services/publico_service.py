import requests
from flask import current_app


def _base_url():
    return current_app.config.get("API_BASE_URL", "http://localhost:5000/api")


def get_inicio():
    """
    Llama a GET /inicio.
    Retorna (datos, None) o (None, mensaje_error).
    """
    try:
        res = requests.get(f"{_base_url()}/inicio", timeout=10)
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
        res = requests.get(f"{_base_url()}/menu", timeout=10)
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
        res = requests.get(f"{_base_url()}/reviews", timeout=10)
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
            f"{_base_url()}/reservas/{id_reserva}/review",
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

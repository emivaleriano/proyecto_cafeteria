import re
from backend.utils.respuestas import (
    HTTP_BAD_REQUEST_CODE,
    MENSAJE_SOLICITUD_INVALIDA,
    crear_error
)

def validar_id(id):
    """Valida que el ID sea un número entero positivo."""
    if not id:
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, "El ID no puede estar vacío")
        ])
    try:
        id_ = int(id)
    except ValueError:
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, f"El ID '{id}' no es un número válido")
        ])
    if id_ <= 0:
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, f"El ID '{id_}' debe ser mayor a 0")
        ])
    return id_


def validar_texto(texto, nombre_campo="campo"):
    """Valida que un texto no esté vacío."""
    if not texto or not texto.strip():
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, f"El campo '{nombre_campo}' no puede estar vacío")
        ])
    return texto.strip()


def validar_email(email):
    """Valida formato básico de email."""
    if not email:
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, "El email no puede estar vacío")
        ])
    patron = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    if not patron.match(email):
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, f"El email '{email}' no tiene un formato válido")
        ])
    return email


def validar_entero_positivo(valor, nombre_campo="valor"):
    """Valida que un valor sea entero y positivo."""
    try:
        numero = int(valor)
    except (ValueError, TypeError):
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, f"El campo '{nombre_campo}' debe ser un número entero")
        ])
    if numero < 0:
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, f"El campo '{nombre_campo}' no puede ser negativo")
        ])
    return numero


def validar_fecha(fecha_str):
    """Valida que la fecha tenga formato YYYY-MM-DD."""
    if not fecha_str:
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, "La fecha no puede estar vacía")
        ])
    patron = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not patron.match(fecha_str):
        raise RuntimeError([
            crear_error(HTTP_BAD_REQUEST_CODE, MENSAJE_SOLICITUD_INVALIDA, f"La fecha '{fecha_str}' no tiene el formato YYYY-MM-DD")
        ])
    return fecha_str

def validar_estrellas(estrellas):
    """Valida que estrellas sea un entero entre 1 y 5"""
    if not isinstance(estrellas, int) or not (1 <= estrellas <= 5):
        raise ValueError("'estrellas' debe ser un número entero entre 1 y 5")
    return estrellas

def validar_comentario(comentario):
    """Valida que el comentario sea un string no vacío"""
    if not comentario or not isinstance(comentario, str) or not comentario.strip():
        raise ValueError("'comentario' no puede estar vacío")
    return comentario.strip()

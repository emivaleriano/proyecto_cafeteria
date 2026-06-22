import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import bcrypt
import jwt
from flask import request

from backend.utils.respuestas import (
    crear_respuesta_error,
    HTTP_UNAUTHORIZED_CODE,
)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXP_HORAS = int(os.getenv("JWT_EXP_HORAS", 1))


# --- contraseña -----

def hashear_password(password: str) -> str:
    """Genera un hash bcrypt de la contrasena en texto plano"""
    hash_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")

def verificar_password(password: str, password_hash: str) -> bool:
    """Compara la password en texto plano con el hash de bcrypt"""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


# JWT

def generar_token(admin_id: int) -> str:
    """Genera un JWT firmado con el id del admin."""
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": str(admin_id),
        "iat": ahora,
        "exp": ahora + timedelta(hours=JWT_EXP_HORAS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decodificar_token(token: str) -> dict:
    """Decodifica un JWT y devuelve su payload. Lanza ValueError si falla."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token invalido")

# Decorador

def requiere_admin(funcion):
    """Decorador que valida el JWT del header Authorization."""
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return crear_respuesta_error(
                HTTP_UNAUTHORIZED_CODE,
                "Token faltante",
                "Debe enviar el header Authorization con formato 'Bearer <token>'",
            )

        token = header[len("Bearer "):].strip()

        try:
            payload = decodificar_token(token)
        except ValueError as e:
            return crear_respuesta_error(HTTP_UNAUTHORIZED_CODE, "Token invalido", str(e))

        request.admin_actual = payload
        return funcion(*args, **kwargs)

    return wrapper

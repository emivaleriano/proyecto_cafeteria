import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

def generar_token_resena(id_reserva):
    payload = {
        "id_reserva": id_reserva,
        "exp": datetime.now(timezone.utc) + timedelta(days=7) # dura una semana despues Complete la reserva y se mande el mail con el link generado
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def verificar_token_resena(token):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload["id_reserva"], None
    except jwt.ExpiredSignatureError:
        return None, "El link de reseña venció."
    except jwt.InvalidTokenError:
        return None, "El link de reseña no es válido."

def generar_token_edicion_resena(id_resena):
    payload = {
        "id_resena": id_resena,
        "exp": datetime.now(timezone.utc) + timedelta(days=90)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def verificar_token_edicion_resena(token):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload["id_resena"], None
    except jwt.ExpiredSignatureError:
        return None, "El link de edición venció."
    except jwt.InvalidTokenError:
        return None, "El link de edición no es válido."
from functools import wraps

from flask import redirect, session, url_for

from frontend.services.admin_service import validar_token

def requiere_sesion(funcion):
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        token = session.get("admin_token")
        if not token:
            return redirect(url_for("admin.login"))

        datos, error = validar_token(token)
        if error:
            session.clear()
            return redirect(url_for("admin.login"))

        return funcion(*args, **kwargs)
    return wrapper

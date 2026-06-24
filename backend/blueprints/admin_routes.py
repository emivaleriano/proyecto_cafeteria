from flask import Blueprint, request
from backend.services.admin_service import autenticar_admin, cambiar_contrasenia
from backend.services.reservas_service import obtener_todas_reservas
from backend.services.dashboard_service import obtener_stats
from backend.repositories.menu_repository import obtener_menu
from backend.repositories.servicios_repository import obtener_servicios
from backend.utils.admin import requiere_admin
from backend.utils.respuestas import (
    crear_respuesta_error,
    crear_respuesta_exito,
    HTTP_BAD_REQUEST_CODE,
    HTTP_UNAUTHORIZED_CODE,
    HTTP_INTERNAL_ERROR_CODE,
    HTTP_OK_CODE
)



admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    usuario = data.get("usuario")
    contrasenia = data.get("contrasenia")

    if not usuario or not contrasenia:
        return crear_respuesta_error(
            HTTP_BAD_REQUEST_CODE,
            "Datos faltantes",
            "Usuario y contraseña son requeridos",
        )

    try:
        datos = autenticar_admin(usuario, contrasenia)
    except Exception as e:
        return crear_respuesta_error(HTTP_INTERNAL_ERROR_CODE, "Error interno", str(e))

    if datos is None:
        return crear_respuesta_error(
            HTTP_UNAUTHORIZED_CODE,
            "Credenciales invalidas",
            "Usuario o contraseña incorrectos",
        )

    return crear_respuesta_exito(datos=datos, mensaje="Login exitoso")


@admin_bp.route("/me", methods=['GET'])
@requiere_admin
def me():
    return crear_respuesta_exito(
        datos={"id_admin": request.admin_actual["sub"]},
        mensaje="Token valido",
    )


@admin_bp.route("/contrasenia", methods=["PATCH"])
@requiere_admin
def patch_contrasenia():
    data = request.get_json(silent=True) or {}

    contra_actual = data.get("contra_actual")
    nueva_contra  = data.get("nueva_contra")

    if not contra_actual or not nueva_contra:
        return crear_respuesta_error(
            HTTP_BAD_REQUEST_CODE,
            "Datos faltantes",
            "Contraseña actual y nueva contraseña son requeridas",
        )

    id_admin = request.admin_actual["sub"]

    cambiar_contrasenia(id_admin, contra_actual, nueva_contra)

    return crear_respuesta_exito(mensaje="Contraseña actualizada.", codigo=HTTP_OK_CODE)


@admin_bp.route("/dashboard", methods=['GET'])
@requiere_admin
def dashboard_data():
    pagina = int(request.args.get("pagina", 1))
    orden = request.args.get("orden", "asc")
    estados = request.args.getlist("estado")

    stats = obtener_stats()
    reservas = obtener_todas_reservas(pagina=pagina, orden=orden, estados=estados)
    platos = obtener_menu()
    servicios = obtener_servicios()

    datos = {
        "stats": stats,
        "reservas": reservas,
        "platos": platos,
        "servicios": servicios
    }
    return crear_respuesta_exito(datos=datos, mensaje="Dashboard obtenido")

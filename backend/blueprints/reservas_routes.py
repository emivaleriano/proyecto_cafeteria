from flask import Blueprint, request
from backend.utils.admin import requiere_admin
from backend.services.reservas_service import (
    crear_nueva_reserva,
    data_obtener_reserva,
    data_cancelar_reserva,
    data_actualizar_estado_reserva,
    data_obtener_todas_reservas,
    data_check_in,
    data_actualizar_reservas_vencidas,
)

from backend.utils.respuestas import (
    crear_respuesta_exito,
    crear_respuesta_error,
    HTTP_OK_CODE,
    HTTP_NOT_FOUND_CODE,
    HTTP_CREATED_CODE,
    HTTP_BAD_REQUEST_CODE,
    MENSAJE_NO_ENCONTRADO
)

reservas_bp = Blueprint("reservas", __name__)


@reservas_bp.route("/reservas", methods=["POST"])
def crear_reserva_route():
    data = request.get_json(silent=True)
    if not data:
        return crear_respuesta_error(
            codigo=HTTP_BAD_REQUEST_CODE,
            descripcion="Body inválido",
            mensaje="Se esperaba un cuerpo JSON con los datos de la reserva"
        )

    resultado = crear_nueva_reserva(data)

    return crear_respuesta_exito(
        datos=resultado,
        mensaje="Reserva creada correctamente",
        codigo=HTTP_CREATED_CODE
    )



@reservas_bp.route("/reservas/<int:id>", methods=["GET"])
def obtener_reserva_route(id):

    reserva = data_obtener_reserva(id)

    if not reserva:

        return crear_respuesta_error(
            codigo=HTTP_NOT_FOUND_CODE,
            descripcion=MENSAJE_NO_ENCONTRADO,
            mensaje="No existe una reserva con ese id"
        )

    return crear_respuesta_exito(
        datos=reserva,
        mensaje="Reserva obtenida correctamente",
        codigo=HTTP_OK_CODE
    )


@reservas_bp.route("/reservas/<int:id>/cancelar", methods=["PATCH"])
def cancelar_reserva_route(id):

    resultado = data_cancelar_reserva(id)

    if "error" in resultado:

        return crear_respuesta_error(
            codigo=HTTP_BAD_REQUEST_CODE,
            descripcion="No se pudo cancelar la reserva",
            mensaje=resultado["error"]
        )

    return crear_respuesta_exito(
        datos={"id_reserva": id},
        mensaje="Reserva cancelada correctamente",
        codigo=HTTP_OK_CODE
    )


@reservas_bp.route("/reservas", methods=["GET"])
@requiere_admin
def obtener_reservas_route():
    pagina = int(request.args.get("pagina", 1))
    max = int(request.args.get("max", 10))
    estados = request.args.getlist("estado")
    orden = request.args.get("orden", "asc")
    resultado = data_obtener_todas_reservas(pagina, max, estados, orden)
    return crear_respuesta_exito(
        datos=resultado,
        mensaje="Reservas obtenidas correctamente",
        codigo=HTTP_OK_CODE
    )

@reservas_bp.route("/reservas/<int:id>/estado", methods=["PATCH"])
def actualizar_estado_route(id):
    data = request.get_json(silent=True) or {}
    estado = data.get("estado")
    resultado = data_actualizar_estado_reserva(id, estado)
    if "error" in resultado:
        return crear_respuesta_error(
            codigo=HTTP_BAD_REQUEST_CODE,
            descripcion="No se pudo actualizar la reserva",
            mensaje=resultado["error"]
        )
    return crear_respuesta_exito(
        datos={"id_reserva": id},
        mensaje="Reserva actualizada correctamente",
        codigo=HTTP_OK_CODE
    )

@reservas_bp.route("/reservas/check-in/<string:token>", methods=["GET"])
def obtener_check_in_route(token):
    resultado = data_check_in(token)
    if "error" in resultado:
        return crear_respuesta_error(
            codigo=HTTP_BAD_REQUEST_CODE,
            descripcion="No se pudo obtener la reserva",
            mensaje=resultado["error"]
        )
    return crear_respuesta_exito(
        datos=resultado,
        mensaje="Reserva obtenida correctamente",
        codigo=HTTP_OK_CODE
    )

@reservas_bp.route("/reservas/actualizar-vencidas", methods=["PATCH"])
@requiere_admin
def actualizar_reservas_vencidas():
    cantidad = data_actualizar_reservas_vencidas()
    return crear_respuesta_exito(
        datos={"actualizadas": cantidad},
        mensaje=f"Se actualizaron {cantidad} reserva(s) vencida(s)."
    )

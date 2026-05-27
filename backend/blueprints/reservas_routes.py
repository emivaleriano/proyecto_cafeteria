from flask import Blueprint, request

from backend.services.reservas_service import (
    data_crear_reserva,
    data_obtener_reserva,
    data_cancelar_reserva
)

from backend.utils.respuestas import (
    crear_respuesta_exito,
    crear_error,
    HTTP_OK_CODE,
    HTTP_NOT_FOUND_CODE,
    HTTP_CREATED_CODE,
    HTTP_BAD_REQUEST_CODE,
    MENSAJE_NO_ENCONTRADO
)

reservas_bp = Blueprint("reservas", __name__)


@reservas_bp.route("/reservas", methods=["POST"])
def crear_reserva_route():

    data = request.get_json()

    resultado = data_crear_reserva(data)

    if "error" in resultado:

        error = crear_error(
            codigo=HTTP_BAD_REQUEST_CODE,
            descripcion="Sin disponibilidad",
            mensaje=resultado["error"]
        )

        return error, HTTP_BAD_REQUEST_CODE

    return crear_respuesta_exito(
        datos=resultado,
        mensaje="Reserva creada correctamente",
        codigo=HTTP_CREATED_CODE
    )


@reservas_bp.route("/reservas/<int:id>", methods=["GET"])
def obtener_reserva_route(id):

    reserva = data_obtener_reserva(id)

    if not reserva:

        error = crear_error(
            codigo=HTTP_NOT_FOUND_CODE,
            descripcion=MENSAJE_NO_ENCONTRADO,
            mensaje="No existe una reserva con ese id"
        )

        return error, HTTP_NOT_FOUND_CODE

    return crear_respuesta_exito(
        datos=reserva,
        mensaje="Reserva obtenida correctamente",
        codigo=HTTP_OK_CODE
    )


@reservas_bp.route("/reservas/<int:id>/cancelar", methods=["PATCH"])
def cancelar_reserva_route(id):

    resultado = data_cancelar_reserva(id)

    if "error" in resultado:

        error = crear_error(
            codigo=HTTP_NOT_FOUND_CODE,
            descripcion=MENSAJE_NO_ENCONTRADO,
            mensaje=resultado["error"]
        )

        return error, HTTP_NOT_FOUND_CODE

    return crear_respuesta_exito(
        datos={"id": id},
        mensaje="Reserva cancelada correctamente",
        codigo=HTTP_OK_CODE
    )
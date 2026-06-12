from flask import Blueprint, request, jsonify
from backend.utils.admin import requiere_admin
from backend.utils.respuestas import (
    HTTP_OK_CODE, HTTP_INTERNAL_ERROR_CODE,
    crear_respuesta_exito, crear_error,
)
from backend.services.inicio_service import (
    obtener_info_local,
    obtener_resenas,
    crear_resena,
    actualizar_info_local
)

inicio_bp = Blueprint("/", __name__)


"""/inicio: Devuelve la informacion general del local"""
@inicio_bp.route("/inicio", methods=["GET"])
def get_inicio():
    try:
        data = obtener_info_local()
        return crear_respuesta_exito(
            datos=data,
            mensaje="Información del local obtenida correctamente",
            codigo=HTTP_OK_CODE,
        )
    except Exception as e:
        return crear_error(
            codigo=HTTP_INTERNAL_ERROR_CODE,
            descripcion="Error al obtener información del local",
            mensaje=str(e),
            nivel="error",
        ), HTTP_INTERNAL_ERROR_CODE


"""/reviews: Devuelve las reseñas publicadas"""
@inicio_bp.route("/reviews", methods=["GET"])
def get_reviews():
    try:
        resenas = obtener_resenas()
        return crear_respuesta_exito(
            datos=resenas,
            mensaje="Reseñas obtenidas correctamente",
            codigo=HTTP_OK_CODE,
        )
    except Exception as e:
        return crear_error(
            codigo=HTTP_INTERNAL_ERROR_CODE,
            descripcion="Error al obtener reseñas",
            mensaje=str(e),
            nivel="error",
        ), HTTP_INTERNAL_ERROR_CODE


"""/reservas/<id_reserva>/review: Permite publicar una reseña para una reserva completada"""
@inicio_bp.route("/reservas/<int:id_reserva>/review", methods=["POST"])
def post_review(id_reserva):
    try:
        body = request.get_json(silent=True)
        if not body:
            return crear_error(400, "Body inválido", "Se esperaba JSON"), 400

        estrellas  = body.get("estrellas")
        comentario = body.get("comentario")

        try:
            nuevo_id = crear_resena(id_reserva, estrellas, comentario)
        except LookupError as le:
            return crear_error(404, "No encontrada", str(le)), 404
        except ValueError as ve:
            msg = str(ve)
            codigo = 409 if "Ya existe" in msg else 400
            return crear_error(codigo, "Datos inválidos", msg), codigo

        return crear_respuesta_exito(
            datos={"id_resena": nuevo_id},
            mensaje="Reseña creada exitosamente",
            codigo=201,
        )

    except Exception as e:
        return crear_error(
            codigo=HTTP_INTERNAL_ERROR_CODE,
            descripcion="Error al crear la reseña",
            mensaje=str(e),
            nivel="error",
        ), HTTP_INTERNAL_ERROR_CODE

@inicio_bp.route("/admin/inicio/config", methods=["PUT"])
@requiere_admin
def put_info_local():
    data = request.get_json(silent=True) or {}
    nombre = data.get("nombre")
    direccion = data.get("direccion")
    telefono = data.get("telefono")
    email = data.get("email")
    capacidad = data.get("capacidad")

    actualizar_info_local(nombre, direccion, telefono, email, capacidad)
    respuesta, codigo = crear_respuesta_exito(mensaje="Información del local modificada", codigo=HTTP_OK_CODE)
    return jsonify(respuesta), codigo

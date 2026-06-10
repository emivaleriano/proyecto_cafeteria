from flask import Blueprint, request, jsonify
from backend.services.servicios_service import (
    obtener_servicios,
    obtener_servicios_activos,
    agregar_servicio,
    eliminar_servicio,
    obtener_servicio,
    modificar_servicio,
    activar_desactivar_servicio,

)
from backend.utils.respuestas import (
    crear_respuesta_exito,
    HTTP_CREATED_CODE,
    HTTP_NO_CONTENT_CODE,
    HTTP_OK_CODE,

)

from backend.utils.admin import requiere_admin


servicios_bp = Blueprint("servicios", __name__)

@servicios_bp.route("/", methods=["GET"])
@requiere_admin
def get_servicios():
    """Devuelve tanto los servicios activos, como los inactivos."""
    datos = obtener_servicios()
    respuesta, codigo = crear_respuesta_exito(datos=datos)
    return jsonify(respuesta), codigo


@servicios_bp.route("/activos", methods=["GET"])
def get_servicios_activos():
    """Devuelve solo los servicios activos. No requiere admin porque se usa en las consultas de las reservas"""
    datos = obtener_servicios_activos()
    respuesta, codigo = crear_respuesta_exito(datos=datos)
    return jsonify(respuesta), codigo


@servicios_bp.route("/", methods=["POST"])
@requiere_admin
def post_servicio():
    """Crea un nuevo servicio. Solo esta autorizado el admin"""
    data = request.get_json(silent=True) or {}
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    activo = data.get("activo", True)
    agregar_servicio(nombre, descripcion, activo)
    respuesta, codigo = crear_respuesta_exito(
        mensaje="Servicio creado",
        codigo=HTTP_CREATED_CODE,
    )
    return jsonify(respuesta), codigo

@servicios_bp.route("/<int:id>", methods=["GET"])
def get_servicio(id):
    servicio = obtener_servicio(id)
    respuesta, codigo = crear_respuesta_exito(datos=servicio)
    return jsonify(respuesta), codigo


# decidir si requiere admin o si muestro solo los activos

@servicios_bp.route("/<int:id>", methods=["DELETE"])
@requiere_admin
def delete_servicio(id):
    eliminar_servicio(id)
    return "", HTTP_NO_CONTENT_CODE


@servicios_bp.route("/<int:id>", methods=["PUT"])
@requiere_admin
def update_servicio(id):
    data = request.get_json(silent=True) or {}
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    activo = data.get("activo")

    modificar_servicio(id, nombre, descripcion, activo)
    respuesta, codigo = crear_respuesta_exito(mensaje="Servicio Modificado", codigo=HTTP_OK_CODE)
    return jsonify(respuesta), codigo

@servicios_bp.route("/<int:id>", methods=["PATCH"])
@requiere_admin
def update_activo(id):
    nuevo_estado = activar_desactivar_servicio(id)
    respuesta, codigo = crear_respuesta_exito(datos={"activo": nuevo_estado}, mensaje="Servicio Modificado", codigo=HTTP_OK_CODE)
    return jsonify(respuesta), codigo

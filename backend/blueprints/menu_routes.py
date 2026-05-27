from flask import Blueprint, request
from backend.services.menu_service import listar_menu, data_nuevo_producto, data_modificacion_producto, data_eliminar_producto
from backend.utils.respuestas import (
    crear_respuesta_exito,
    crear_error,
    HTTP_OK_CODE,
    HTTP_NOT_FOUND_CODE,
    MENSAJE_NO_ENCONTRADO,
    HTTP_CREATED_CODE
)

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/menu", methods=["GET"])
def obtener_menu_route():

    menu = listar_menu()

    return crear_respuesta_exito(
        datos=menu,
        mensaje="Menu obtenido correctamente"
    )

@menu_bp.route("/admin/menu", methods=["POST"])
def nuevo_producto():
    data = request.get_json()
    id_producto = data_nuevo_producto(data)

    return crear_respuesta_exito(
        datos={"id": id_producto},
        mensaje="Producto creado correctamente",
        codigo=HTTP_CREATED_CODE
    )

@menu_bp.route("/admin/menu/<int:id>", methods=["PUT"])
def cambios_producto(id):

    data = request.get_json()

    filas_modificadas = data_modificacion_producto(id, data)

    if filas_modificadas == 0:

        error = crear_error(
            codigo=HTTP_NOT_FOUND_CODE,
            descripcion=MENSAJE_NO_ENCONTRADO,
            mensaje="No existe un producto con ese id"
        )

        return error, HTTP_NOT_FOUND_CODE

    return crear_respuesta_exito(
        datos={"id": id},
        mensaje="Producto modificado correctamente",
        codigo=HTTP_OK_CODE
    )

@menu_bp.route("/admin/menu/<int:id>", methods=["DELETE"])
def eliminacion_producto(id):

    filas_eliminadas = data_eliminar_producto(id)

    if filas_eliminadas == 0:

        error = crear_error(
            codigo=HTTP_NOT_FOUND_CODE,
            descripcion=MENSAJE_NO_ENCONTRADO,
            mensaje="No existe un producto con ese id"
        )

        return error, HTTP_NOT_FOUND_CODE

    return crear_respuesta_exito(
        datos={"id": id},
        mensaje="Producto eliminado correctamente",
        codigo=HTTP_OK_CODE
    )
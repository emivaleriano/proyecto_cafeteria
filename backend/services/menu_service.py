import json
from backend.repositories.menu_repository import obtener_menu_activo, crear_producto, modificar_producto, eliminar_producto, obtener_plato

def listar_menu():
    return obtener_menu_activo()

def data_obtener_plato(id):
    plato  = obtener_plato(id)
    if not plato:
        raise LookupError("Plato no encontrado")
    return plato

def data_nuevo_producto(data):
    tags_json = json.dumps(data.get("tags", []))
    return crear_producto(
        data["nombre"],
        data["descripcion"],
        data["precio"],
        data["categoria"],
        tags_json,
        data["imagen"]
    )

def data_modificacion_producto(id_producto, data):
    # pasa los tags a un json para meter al
    tags_json = json.dumps(data.get("tags")) if isinstance(data.get("tags"), list) else (data.get("tags") or "[]")
    return modificar_producto(
        id_producto,
        data["nombre"],
        data["descripcion"],
        data["precio"],
        data["categoria"],
        tags_json,
        data["imagen"],
        data.get("activo", True)
    )


def data_eliminar_producto(id_producto):
    return eliminar_producto(id_producto)

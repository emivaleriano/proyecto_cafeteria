from backend.repositories.menu_repository import obtener_menu_activo, crear_producto, modificar_producto, eliminar_producto

def listar_menu():
    return obtener_menu_activo()

def data_nuevo_producto(data):

    return crear_producto(
        data["nombre"],
        data["descripcion"],
        data["precio"],
        data["categoria"],
        data.get("tags"),
        data["imagen"]
    )

def data_modificacion_producto(id_producto, data):

    return modificar_producto(
        id_producto,
        data["nombre"],
        data["descripcion"],
        data["precio"],
        data["categoria"],
        data.get("tags"),
        data["imagen"],
        data.get("activo", True)
    )


def data_eliminar_producto(id_producto):
    return eliminar_producto(id_producto)

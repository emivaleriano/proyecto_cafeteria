from backend.repositories.servicios_repository import (
    obtener_servicios as repo_obtener_servicios,
    obtener_servicios_activos as repo_obtener_servicios_activos,
    obtener_servicio_por_nombre,
    obtener_servicio_bd,
    agregar_servicio_bd,
    eliminar_servicio_bd,
    modificar_servicio_bd,
    activar_desactivar_servicio_bd,
)



def obtener_servicios():
    """ Devuelve todos los servicios existentes"""
    return repo_obtener_servicios()

def obtener_servicio(id):
    servicio = obtener_servicio_bd(id)
    if not servicio:
        raise LookupError("No existe un servicio con ese ID")
    return servicio

def obtener_servicios_activos():
    """ Devuelve todos los servicios activos"""
    return repo_obtener_servicios_activos()

def agregar_servicio(nombre, descripcion, activo=True):
    """Agrega un servicio si no existe uno con el mismo nombre. Lo inserta como activo por default"""
    nombre = (nombre or "").strip()  #evita espacios al inicio o al final
    descripcion = (descripcion or "").strip()
    if not nombre or not descripcion:
        raise ValueError("Nombre y descripcion son obligatorios")
    if obtener_servicio_por_nombre(nombre) is not None:
        raise KeyError("Ya existe un servicio con ese nombre")
    agregar_servicio_bd(nombre, descripcion, activo)

def eliminar_servicio(id):
    """Elimina un servicio a partir de su id"""
    servicio = obtener_servicio_bd(id)
    if not servicio:
        raise LookupError("No existe un servicio con ese id")

    eliminar_servicio_bd(id)

def modificar_servicio(id, nombre, descripcion, activo):
    nombre = (nombre or "").strip()  #evita espacios al inicio o al final
    descripcion = (descripcion or "").strip()
    if not nombre or not descripcion or activo is None:
        raise ValueError("Faltan datos obligatorios: nombre, descripcion, activo")
    servicio = obtener_servicio_por_nombre(nombre)
    if servicio:
        raise KeyError("Ya existe servicio con ese nombre")
    servicio = obtener_servicio_bd(id)
    if not servicio:
        raise LookupError("No existe un servicio con ese ID")
    modificar_servicio_bd(id, nombre, descripcion, activo)

def activar_desactivar_servicio(id):
    servicio = obtener_servicio_bd(id)
    if not servicio:
        raise LookupError("No existe un servicio con ese ID")
    if bool(servicio.get("activo")):
        activo = False
    else:
        activo = True
    activar_desactivar_servicio_bd(id, activo)
    return activo

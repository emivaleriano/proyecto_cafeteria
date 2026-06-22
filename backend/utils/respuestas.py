HTTP_OK_CODE = 200
HTTP_CREATED_CODE = 201
HTTP_NO_CONTENT_CODE = 204
HTTP_BAD_REQUEST_CODE = 400
HTTP_UNAUTHORIZED_CODE = 401
HTTP_FORBIDDEN_CODE = 403
HTTP_NOT_FOUND_CODE = 404
HTTP_CONFLICT_CODE = 409
HTTP_INTERNAL_ERROR_CODE = 500

MENSAJE_OK = "OK"
MENSAJE_CREADO = "Creado exitosamente"
MENSAJE_SIN_CONTENIDO = "Sin contenido"
MENSAJE_SOLICITUD_INVALIDA = "Solicitud incorrecta"
MENSAJE_NO_AUTORIZADO = "No autorizado"
MENSAJE_PROHIBIDO = "Acceso prohibido"
MENSAJE_NO_ENCONTRADO = "Recurso no encontrado"
MENSAJE_CONFLICTO = "Conflicto con el estado actual"
MENSAJE_ERROR_INTERNO = "Error interno del servidor"


def crear_error(codigo, descripcion, mensaje, nivel="error"):
    """
    Crea un diccionario de error estandarizado.

    Args:
        codigo (int): Código HTTP (ej: 400)
        descripcion (str): Descripción corta del tipo de error
        mensaje (str): Mensaje detallado para el usuario
        nivel (str): "error", "warning", "info"

    Returns:
        dict: Diccionario con la estructura de error
    """
    return {
        "codigo": codigo,
        "descripcion": descripcion,
        "mensaje": mensaje,
        "nivel": nivel
    }


def crear_respuesta_error(codigo, descripcion, mensaje, nivel="error"):
    """
    Crea una respuesta de error estandarizada con el mismo sobre que las
    respuestas exitosas: {exito, mensaje, datos}.

    Returns:
        tuple: (diccionario, codigo_http)
    """
    error = crear_error(codigo, descripcion, mensaje, nivel)
    respuesta = {
        "exito": False,
        "mensaje": mensaje,
        "datos": error,
    }
    return respuesta, codigo


def crear_respuesta_exito(datos=None, mensaje="OK", codigo=200):
    """
    Crea una respuesta exitosa estandarizada.

    Args:
        datos: Datos a devolver (dict, list, etc.)
        mensaje (str): Mensaje descriptivo
        codigo (int): Código HTTP

    Returns:
        tuple: (diccionario, codigo_http)
    """
    respuesta = {
        "exito": True,
        "mensaje": mensaje,
        "datos": datos
    }
    return respuesta, codigo

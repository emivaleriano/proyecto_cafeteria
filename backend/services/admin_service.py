from backend.repositories.admin_repository import obtener_admin_por_usuario
from backend.utils.admin import verificar_password, generar_token

def autenticar_admin(usuario, contrasenia):
    """Verifica los datos del admin y devuelve el token si son validos, None si son invalidos"""
    admin = obtener_admin_por_usuario(usuario)
    if not admin or not verificar_password(contrasenia, admin["contrasenia"]):
        return None

    token = generar_token(admin["id_admin"])
    return {
        "access_token":token,
        "usuario":admin["usuario"],
    }

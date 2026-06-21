from backend.repositories.admin_repository import obtener_admin_por_usuario, actualizar_contrasenia, obtener_admin_por_id
from backend.utils.admin import verificar_password, generar_token, hashear_password

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

def cambiar_contrasenia(id_admin, contra_actual, nueva_contra):
    if len(nueva_contra)<8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")

    admin = obtener_admin_por_id(id_admin)
    if not admin:
        raise LookupError("Administrador no encontrado")

    if not verificar_password(contra_actual, admin["contrasenia"]):
        raise ValueError("La contraseña es incorrecta")

    hash_pass = hashear_password(nueva_contra)
    actualizar_contrasenia(id_admin, hash_pass)

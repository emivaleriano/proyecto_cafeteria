from backend.db import obtener_conexion

def obtener_admin_por_usuario(usuario):
    """Busca un admin a partir de su nombre de usuario
    Devuelve su id, usuario y contraseña (hash) o None si no existe"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_admin, usuario, contrasenia from administrador where usuario = %s",
            (usuario,),
            )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

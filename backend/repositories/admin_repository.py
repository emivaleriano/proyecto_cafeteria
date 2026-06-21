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

def obtener_admin_por_id(id_admin):
    """Busca un admin a partir de su nombre de usuario
    Devuelve su id, usuario y contraseña (hash) o None si no existe"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_admin, usuario, contrasenia from administrador where id_admin = %s",
            (id_admin,),
            )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def actualizar_contrasenia(id_admin, nueva_contra):
    """Cambia la contraseña de un administrador, En el sistema hay uno solo, no se crean mas administradores
    Pero si en algun momento se desea ampliar para que haya, esta funcion sirve"""
    conn=obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "UPDATE administrador SET contrasenia=%s WHERE id_admin= %s", (nueva_contra, id_admin)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

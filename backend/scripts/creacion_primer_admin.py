"""
Script para crear el primer admin con credenciasles admin, admin en la base de datos
Ejecutar (desde la raiz del repo): python -m backend.scripts.creacion_primer_admin
"""
from dotenv import load_dotenv
load_dotenv()

from backend.db import obtener_conexion  # noqa: E402
from backend.utils.admin import hashear_password # noqa: E402
# los imports necesitan las variables ya cargadas

USUARIO_DEFAULT = "admin"
CONTRASENIA_DEFAULT = "admin"

def crear_admin_default():
    hash_pass = hashear_password(CONTRASENIA_DEFAULT)

    conn = obtener_conexion()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO administrador (usuario, contrasenia) VALUES (%s, %s)",
            (USUARIO_DEFAULT, hash_pass),
        )
        conn.commit()
        print(f"Admin '{USUARIO_DEFAULT}' creado correctamente")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    crear_admin_default()

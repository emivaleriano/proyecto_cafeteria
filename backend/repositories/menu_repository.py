from backend.db import obtener_conexion
import json

def obtener_menu_activo():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM menu WHERE activo = true")
        productos = cursor.fetchall()
        for producto in productos:
            if producto["tags"]:
                producto["tags"] = json.loads(producto["tags"]) #pasa los tags a una lista en python para que se vea bien el front

        return productos

    finally:
        cursor.close()
        conn.close()

def crear_producto(nombre, descripcion, precio, categoria, tags, imagen, activo):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("INSERT INTO menu (nombre, descripcion, precio, categoria, tags, imagen, activo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        ,(nombre, descripcion, precio, categoria, tags, imagen, activo)
        )
        conn.commit()
        return cursor.lastrowid

    finally:
        cursor.close()
        conn.close()

def modificar_producto(nombre, descripcion, precio, categoria, tags, imagen, activo, id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("UPDATE menu SET nombre = %s, descripcion = %s, precio = %s, categoria = %s, tags = %s, imagen = %s, activo = %s WHERE id = %s"
        ,(nombre, descripcion, precio, categoria, tags, imagen, activo, id_producto))
        conn.commit()
        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()


def eliminar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("DELETE FROM menu WHERE id = %s",(id_producto,))
        conn.commit()
        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()

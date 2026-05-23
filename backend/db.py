import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv('MYSQL_HOST', 'localhost')
DATABASE_USERNAME = os.getenv('MYSQL_USERNAME', 'root')
DATABASE_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
DATABASE_NAME = os.getenv('MYSQL_DATABASE', 'cafeteria')
DATABASE_PORT = os.getenv('MYSQL_PORT', 3306)

def obtener_conexion():
    try:
        config = {
            'host': DATABASE_HOST,
            'user': DATABASE_USERNAME,
            'password': DATABASE_PASSWORD,
            'database': DATABASE_NAME,
            'port': DATABASE_PORT
        }
        conexion = mysql.connector.connect(**config)
        print("¡Conexión exitosa a MySQL!")
        return conexion

    except mysql.connector.Error as err:
        raise Exception(f"Error en la conexión a la base de datos: {err}")

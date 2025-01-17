"""
Módulo de configuración de la base de datos
-----------------------------------------
Este módulo proporciona la configuración y conexión a la base de datos MySQL.

Clase DatabaseConnection:
    Implementa el patrón Singleton para mantener una única conexión a la base de datos.
    
Métodos:
    get_connection(): Método estático que retorna una conexión a MySQL
        - Gestiona la conexión a la base de datos
        - Maneja errores de conexión
        - Retorna None si la conexión falla
        
Configuración:
    - Host: localhost
    - Usuario: root
    - Contraseña: (vacía)
    - Base de datos: facturacion
"""

import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="facturacion"
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
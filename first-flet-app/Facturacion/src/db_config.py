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
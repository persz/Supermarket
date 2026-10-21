import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv(encoding="latin-1")


class DatabaseManager:

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")

    def get_connection(self):
        """Abre y retorna una nueva conexión a PostgreSQL."""
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
            )
            return connection
        except Exception as e:
            print(f"[-] Error al conectar a la base de datos: {e}")
            return None
from database.db_manager import DatabaseManager
from models.usuario import Usuario


class AuthService:

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.usuario_actual = None  # Guardará la sesión del usuario conectado

    def registrar_usuario(
        self, nombre, correo, password, rol="cliente"
    ) -> bool:
        """Inserta un nuevo usuario en la base de datos PostgreSQL."""
        conn = self.db.get_connection()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO usuarios (nombre, correo, password, rol)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(query, (nombre, correo, password, rol))
            conn.commit()
            print("[+] Usuario registrado exitosamente.")
            return True
        except Exception as e:
            print(f"[-] Error al registrar usuario: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
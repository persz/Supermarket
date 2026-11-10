from database.db_manager import DatabaseManager
from moduls.usuario import Usuario


class AuthService:

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.usuario_actual = None #Guardara la sesión del usuario conectado

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
            print("Usuario registrado exitosamente.")
            return True
        except Exception as e:
            print(f"[-] Error al registrar usuario: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    def iniciar_sesion(self, correo, password):
        conn = self.db.get_connection()
        if not conn:
            return False

        try:
             with conn.cursor() as cursor:
                query = """
                    SELECT id, nombre, correo, password, rol 
                    FROM usuarios 
                    WHERE correo = %s AND password = %s;
                    """
                cursor.execute(query, (correo, password))
                usuario_data = cursor.fetchone()

                if usuario_data:
                    # Creamos el objeto Usuario con los datos de la base de datos
                    self.usuario_actual = Usuario(
                        id=usuario_data[0],
                        nombre=usuario_data[1],
                        correo=usuario_data[2],
                        password=usuario_data[3],
                        rol=usuario_data[4],
                        )
                    print(
                        f"Bienvenido {self.usuario_actual.nombre} ({self.usuario_actual.rol})!"
                        )
                    return True
                else:
                    print("Correo o contraseña incorrectos.")
                    return False

        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return False
        finally:
            conn.close()
    def cerrar_sesion(self):
        self.usuario_actual = None
        print("Sesión cerrada correctamente.")       
         
    

        
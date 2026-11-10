from database.db_manager import DatabaseManager
from moduls.producto import Producto


class InventarioService:

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def agregar_producto(self, nombre, categoria, precio, stock) -> bool:
        """Inserta un nuevo producto en la tabla productos."""
        conn = self.db.get_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO productos (nombre,categoria,precio,stock) VALUES (%s, %s, %s, %s);
                """
            #paso las variables como una tupla    
            cursor.execute(query,(nombre,categoria,precio,stock))
            
            #confirmo la transacion a la db
            conn.commit()
            print(f"[+] producto '{nombre}'  agregado correctamente")
            return True
        except Exception as e:
            print(f"ERROR al agregar el producto {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
                

    def listar_productos(self) -> list:
        """Consulta todos los productos y los devuelve como una lista de objetos Producto."""
        conn = self.db.get_connection()
        if not conn:
            return []
        productos = []
        try:
            with conn.cursor() as cursor:
                query = "SELECT id, nombre, categoria,precio,stoc FROM productos ORDER BY id ASC;"
                cursor.execute(query)
                filas - cursor.fetchall()
                
                for fila in filas:
                    prod = productos(
                        id = fila[0],
                        nombre = fila[1],
                        categoria = fila[2],
                        precio = float(fila[3]),
                        stock = fila[4],
                    )
                    productos.append(prod)
            return productos
        except Exception as e:
            print(f"ERROR al listar los productos {e}")
            return []
        finally:
            conn.close()        
                
                
        
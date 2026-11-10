from database.db_manager import DatabaseManager
from moduls.producto import Producto


class InventarioService:

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def agregar_producto(
        self, nombre: str, categoria: str, precio: float, stock: int
    ) -> bool:
        """Inserta un nuevo producto en la tabla productos."""
        conn = self.db.get_connection()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO productos (nombre, categoria, precio, stock)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(query, (nombre, categoria, precio, stock))

            
            conn.commit()
            print(f"roducto '{nombre}' agregado exitosamente")
            return True

        except Exception as e:
            print(f"ERROR al agregar el producto: {e}")
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
                query = "SELECT id, nombre, categoria, precio, stock FROM productos ORDER BY id ASC;"
                cursor.execute(query)
                filas = (
                    cursor.fetchall()
                )

            #convertimos las tuplas recibidas en objetos Producto
            for fila in filas:
                prod = Producto(
                    id=fila[0],
                    nombre=fila[1],
                    categoria=fila[2],
                    precio=float(fila[3]),
                    stock=fila[4],
                )
                productos.append(prod)

            return productos

        except Exception as e:
            print(f"ERROR al listar los productos: {e}")
            return []
        finally:
            conn.close()     
              
    def actualizar_stock(self,producto_id: int, nuevo_stoc: int)-> bool:
        """Actualiza la cantidad de stock de un producto específico."""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                query = "UPDATE productos SET stock = %s WHERE id = %s;"
                cursor.execute(query,(nuevo_stoc,producto_id))
                
                if cursor.rowcount == 0:
                    print(f"No se encontro ningun producto con id {producto_id}")
                    return False
                
                conn.commit()
                print(f"stock del producto id {producto_id} actualizado")
                return True
            
        except Exception as e:
            print(f"Error al actualizar el stock {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    def eliminar_producto(self,producto_id: int) -> bool:
        """Elimina un producto de la base de datos según su ID."""
        conn = self.db.get_connection()
        if not conn:
            return False
        try:
            with conn.cursor as cursor:
                query = "DELETE FROM productos WHERE ID = %s"
                cursor.execute(query,(producto_id,))\
                    
                if cursor.rowcount == 0:
                    print(f"no se encontro ningun producto con id {producto_id}")
                    return False
                conn.commit()
                print(f"Producto id {producto_id} eliminado con exito del inventario")
                return True
        except Exception as e:
            print(f"ERROR al eliminar el producto {e}")
            conn.rollback()
            return False        
                     
                     
                
                
        
import time
class MenuManager:
    def __init__(self,auth_service, inventario_service):
        self.auth = auth_service
        self.inventario = inventario_service
        
    def iniciar(self):
        while True:
            print("\n" + "=" * 35)
            print("Supermarket Menu")
            print("=" * 35)
            print("1-Inicar sesion") 
            print("2-Registrarse")
            print("3-Salir")
            try:
                opcion = int(input("\n seleciona una opcion (1-3): ").strip())
                match opcion:
                    case 1:
                        self._menu.login()
                    case 2:
                        self._menu.registro()
                    case 3:
                        print("Gracias por utlizar el sistema...")
                        time.sleep(2)
                        break
                    case _:
                        print("Eliga una opcion valida por favor")
            except Exception as e:
                print(f"Error {e}")
                            
    def _menu_login(self):
        print("---Incio de sesion---")
        correo = input("Correo: ").strip()
        password = input("Clave: ").strip()
        
        if self.auth.iniciar_sesion(correo,password):
            usuario = self.auth.usuario_actual
            if usuario.rol == "admin":
                self._menu_admin()
            else:
                self._menu_cliente()
                
    def _menu_registro(self):
        print("---Registro Usuario---")
        nombre = input("Nombre Completo: ").strip()
        correo = input("Correo Eletronico: ").strip()
        password = input("Ingrese su clave: ").strip()
        rol =( input("Rol (cliente/adminm) [Por defecto: cliente]:")).strip().lower()
        
        if not rol:
            rol = "cliente"
        self.auth.registrar_usuario(nombre,correo,password,rol)
        
    def _menu_admin(self):
        while True:
            print("\n" + "-" * 35)
            print(f" PANEL DE ADMINISTRACIÓN ({self.auth.usuario_actual.nombre})")
            print("-" * 35)
            print("1-Agregar Producto")
            print("2-Listar Productos")
            print("3-Actualizar Stock")
            print("4-Eliminar Producto")
            print("5-Cerrar Sesión")
            
            try:
                opcion = int(input("\nSeleccione una opcion (1-5)").strip())
                match opcion:
                    case 1:
                        nombre = input("Nombre del producto: "),strip()
                        categoria = input("Categoria: ").strip()
                        try:
                            precio = float(input("Precio ($): "))  
                            stock = int(input("stock Inicial: "))
                            self.inventario.agregar_producto(nombre,categoria,precio,stock)                  
                        except ValueError:
                            print("El stoc y el precio deben ser numeros")
                    case 2:
                        print("---Catalogo de productos---")
                        productos = self.inventario.listar_productos()
                        if not productos:
                            print("No hay productos en el inventario")
                        else:
                            for p in productos:
                                print(f" {p}")
                    case 3:
                        try:
                            prod_id = int(input("ID del producto a actualizar: "))
                            nuevo_stock  = int(input("Nuevo stock: "))
                            self.inventario.actualizar_stock(prod_id,nuevo_stock)
                        except ValueError:
                            print("ERROR: los id y el stock deben ser enteros")
                    case 4:
                        try:
                            prod_id = int(input("ID del producto que desea eliminar: "))
                            self.inventario.eliminar_producto(prod_id)
                        except ValueError:
                            print("El ID debe ser un entero")
                    case 5:
                        self.auth.cerrar_sesion()
                        break
                    case _:
                        print("Eliga una opcion valida")                 
            
            except Exception as e:
                print(f"ERROR {e}")     
                 
    def _menu_cliente(self):
        while True:
            print("\n" + "-" * 35)
            print(f" PANEL DE CLIENTE ({self.auth.usuario_actual.nombre})")
            print("-" * 35)
            print("1-Ver Catálogo de Productos")
            print("2-Cerrar Sesión")
            try:
                opcion = int(input("Elegia una opcion (1-2): ")).strip()
                match opcion:
                    case 1:
                        print("Productos disponibles")
                        productos = self.inventario.listar_productos()
                        if not productos:
                            print("No hay productos disponibles")
                        else:
                            for p in productos:
                                print(f" {p}")
                    case 2:
                        self.auth.cerrar_sesion()
                    case _:
                        print("Opcion no valida")    
                                         
            except Exception as e:
                print(f"ERROR {e}")    
                                                             
                    
                    
                        
            
           
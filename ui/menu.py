import time


class MenuManager:

    def __init__(self, auth_service, inventario_service, venta_service):
        self.auth = auth_service
        self.inventario = inventario_service
        self.venta = venta_service

    def iniciar(self):
        while True:
            print("\n" + "=" * 35)
            print("         Supermarket Menu")
            print("=" * 35)
            print("1- Iniciar sesión")
            print("2- Registrarse")
            print("3- Salir")
            try:
                opcion = int(input("\nSeleccione una opción (1-3): ").strip())
                match opcion:
                    case 1:
                        self._menu_login()
                    case 2:
                        self._menu_registro()
                    case 3:
                        print("Gracias por utilizar el sistema...")
                        time.sleep(1)
                        break
                    case _:
                        print("Elija una opción válida por favor.")
            except Exception as e:
                print(f"Error: {e}")

    def _menu_login(self):
        print("\n--- Inicio de sesión ---")
        correo = input("Correo: ").strip()
        password = input("Clave: ").strip()

        if self.auth.iniciar_sesion(correo, password):
            usuario = self.auth.usuario_actual
            if usuario.rol == "admin":
                self._menu_admin()
            else:
                self._menu_cliente()

    def _menu_registro(self):
        print("\n--- Registro Usuario ---")
        nombre = input("Nombre Completo: ").strip()
        correo = input("Correo Electrónico: ").strip()
        password = input("Ingrese su clave: ").strip()
        rol = (
            input("Rol (cliente/admin) [Por defecto: cliente]: ")
            .strip()
            .lower()
        )

        if not rol:
            rol = "cliente"
        self.auth.registrar_usuario(nombre, correo, password, rol)

    def _menu_admin(self):
        while True:
            print("\n" + "-" * 35)
            print(f" PANEL DE ADMINISTRACIÓN ({self.auth.usuario_actual.nombre})")
            print("-" * 35)
            print("1- Agregar Producto")
            print("2- Listar Productos")
            print("3- Actualizar Stock")
            print("4- Eliminar Producto")
            print("5- Cerrar Sesión")

            try:
                opcion = int(input("\nSeleccione una opción (1-5): ").strip())
                match opcion:
                    case 1:
                        nombre = input("Nombre del producto: ").strip()
                        categoria = input("Categoría: ").strip()
                        try:
                            precio = float(input("Precio ($): "))
                            stock = int(input("Stock Inicial: "))
                            self.inventario.agregar_producto(
                                nombre, categoria, precio, stock
                            )
                        except ValueError:
                            print(
                                "ERROR: El stock y el precio deben ser números."
                            )

                    case 2:
                        print("\n--- Catálogo de productos ---")
                        productos = self.inventario.listar_productos()
                        if not productos:
                            print("No hay productos en el inventario.")
                        else:
                            for p in productos:
                                print(f"  {p}")

                    case 3:
                        try:
                            prod_id = int(
                                input("ID del producto a actualizar: ")
                            )
                            nuevo_stock = int(input("Nuevo stock: "))
                            self.inventario.actualizar_stock(
                                prod_id, nuevo_stock
                            )
                        except ValueError:
                            print(
                                "ERROR: El ID y el stock deben ser enteros."
                            )

                    case 4:
                        try:
                            prod_id = int(
                                input("ID del producto que desea eliminar: ")
                            )
                            self.inventario.eliminar_producto(prod_id)
                        except ValueError:
                            print("ERROR: El ID debe ser un entero.")

                    case 5:
                        self.auth.cerrar_sesion()
                        break

                    case _:
                        print("Elija una opción válida.")

            except Exception as e:
                print(f"ERROR: {e}")

    def _menu_cliente(self):
        while True:
            print("\n" + "-" * 35)
            print(f" PANEL DE CLIENTE ({self.auth.usuario_actual.nombre})")
            print("-" * 35)
            print("1-Ver Catálogo")
            print("2-Agregar Producto al Carrito")
            print("3-Ver Carrito y Total")
            print("4-Finalizar Compra y Generar Factura")
            print("5-Cerrar Sesión")

            try:
                opcion = int(input("\nElija una opción (1-5): ").strip())
                match opcion:
                    case 1:
                        productos = self.inventario.listar_productos()
                        for p in productos:
                            print(f"  {p}")

                    case 2:
                        productos = self.inventario.listar_productos()
                        if not productos:
                            print("No hay productos disponibles.")
                            continue
                        
                        prod_id = int(input("Ingrese el ID del producto que desea comprar: "))
                        producto_sel = next((p for p in productos if p.id == prod_id), None)

                        if producto_sel:
                            cant = int(input(f"Cantidad para '{producto_sel.nombre}': "))
                            self.venta.agregar_al_carrito(producto_sel, cant)
                        else:
                            print("[-] ID de producto no encontrado.")

                    case 3:
                        self.venta.ver_carrito()

                    case 4:
                        if self.venta.ver_carrito() > 0:
                            confirmar = input("\n¿Desea confirmar su compra? (s/n): ").strip().lower()
                            if confirmar == 's':
                                self.venta.procesar_compra(self.auth.usuario_actual)

                    case 5:
                        self.auth.cerrar_sesion()
                        break
                    case _:
                        print("Opción no válida.")

            except Exception as e:
                print(f"ERROR: {e}")
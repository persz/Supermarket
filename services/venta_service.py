from database.db_manager import DatabaseManager
from services.email_service import EmailFacturasService


class VentaService:

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.email_service = EmailFacturasService()
        self.carrito = (
            []
        )  # Lista de dicts: [{'producto': obj, 'cantidad': int}]

    def agregar_al_carrito(self, producto, cantidad: int) -> bool:
        """Agrega un producto al carrito verificando existencias en stock."""
        if cantidad > producto.stock:
            print(
                f"Stock insuficiente. Solo hay {producto.stock} unidades disponibles."
            )
            return False

        # Si el producto ya está en el carrito, sumamos la cantidad
        for item in self.carrito:
            if item["producto"].id == producto.id:
                if item["cantidad"] + cantidad > producto.stock:
                    print(
                        "Excede la cantidad de stock disponible en el inventario."
                    )
                    return False
                item["cantidad"] += cantidad
                print(
                    f"Se actualizaron las unidades de {producto.nombre} en el carrito."
                )
                return True

        self.carrito.append({"producto": producto, "cantidad": cantidad})
        print(f"{producto.nombre} agregado con éxito al carrito.")
        return True

    def ver_carrito(self) -> float:
        """Despliega los productos del carrito y retorna el total a pagar."""
        if not self.carrito:
            print("\nEl carrito está vacío.")
            return 0.0

        print("\n--- Carrito de compras ---")
        total = 0.0
        for i, item in enumerate(self.carrito, 1):
            p = item["producto"]
            cant = item["cantidad"]
            subtotal = p.precio * cant
            total += subtotal
            print(
                f"{i}. {p.nombre} x{cant} @ ${p.precio:.2f} = ${subtotal:.2f}"
            )
        print(f"TOTAL A PAGAR: ${total:.2f}")
        return total

    def procesar_compra(self, usuario) -> bool:
        """Ejecuta la transacción de compra en PostgreSQL, genera el PDF y envía el correo."""
        if not self.carrito:
            print("El carrito está vacío.")
            return False

        conn = self.db.get_connection()
        if not conn:
            return False

        try:
            total_venta = sum(
                item["producto"].precio * item["cantidad"]
                for item in self.carrito
            )

            with conn.cursor() as cursor:
                # Registrar la venta
                cursor.execute(
                    "INSERT INTO ventas (usuario_id, total) VALUES (%s, %s) RETURNING id;",
                    (usuario.id, total_venta),
                )
                venta_id = cursor.fetchone()[0]

                detalles_factura = []
                # Registrar detalles y actualizar stock de productos
                for item in self.carrito:
                    p = item["producto"]
                    cant = item["cantidad"]
                    subtotal = p.precio * cant

                    cursor.execute(
                        """
                        INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        (venta_id, p.id, cant, p.precio, subtotal),
                    )

                    cursor.execute(
                        "UPDATE productos SET stock = stock - %s WHERE id = %s;",
                        (cant, p.id),
                    )

                    detalles_factura.append({
                        "nombre": p.nombre,
                        "cantidad": cant,
                        "precio": p.precio,
                        "subtotal": subtotal,
                    })

            conn.commit()
            print(f"\n¡Compra procesada exitosamente! Venta #{venta_id}")

            # Generar PDF y enviar factura por correo
            pdf_path = self.email_service.generar_pdf_factura(
                venta_id, usuario.nombre, detalles_factura, total_venta
            )
            print(f"Factura PDF generada en: {pdf_path}")
            

            print(f"[DEBUG] Correo del usuario actual: '{usuario.correo}'")
            self.email_service.enviar_factura_email(
                usuario.correo, usuario.nombre, venta_id, pdf_path
            )

            # Vaciar carrito
            self.carrito.clear()
            return True

        except Exception as e:
            print(f"Error al procesar la compra: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
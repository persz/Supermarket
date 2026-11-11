from database.db_manager import DatabaseManager
from services.auth_service import AuthService
from services.inventario_service import InventarioService
from services.venta_service import VentaService
from ui.menu import MenuManager

def main():
    db = DatabaseManager()

    auth_service = AuthService(db)
    inventario_service = InventarioService(db)
    venta_service = VentaService(db)

    ui = MenuManager(auth_service, inventario_service, venta_service)
    ui.iniciar()


if __name__ == "__main__":
    main()
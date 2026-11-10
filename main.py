from database.db_manager import DatabaseManager
from services.auth_service import AuthService
from services.inventario_service import InventarioService
from ui.menu import MenuManager


def main():
    #Inicializar la base de datos
    db = DatabaseManager()

    #Inicializar servicios
    auth_service = AuthService(db)
    inventario_service = InventarioService(db)

    #Lanzar la interfaz de usuario
    ui = MenuManager(auth_service, inventario_service)

    
    ui.iniciar()


if __name__ == "__main__":
    main()
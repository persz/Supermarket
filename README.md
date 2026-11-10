# Supermarket Virtual - Sistema de Gestión en Consola

Aplicación de consola en Python para la gestión de un supermercado virtual, construida bajo el paradigma de **Programación Orientada a Objetos (POO)** e integrada con una base de datos relacional **PostgreSQL**.

El sistema cuenta con control de acceso basado en roles (`admin` y `cliente`), permitiendo administrar el catálogo de productos y navegar por el inventario disponible.

---

## Características Principales

* **Autenticación y Control de Roles:**
  * Registro e inicio de sesión de usuarios.
  * Roles diferenciados: `admin` (gestión completa) y `cliente` (consulta de catálogo).
* **Gestión de Inventario (CRUD):**
  * Agregar nuevos productos con categoría, precio y stock.
  * Listar el catálogo completo de productos.
  * Actualizar existencias (stock) de productos por ID.
  * Eliminar productos de la base de datos.
* **Arquitectura Modular:**
  * Separación clara entre capa de datos, modelos POO, servicios de negocio e interfaz de consola.
* **Persistencia Segura:**
  * Uso de `psycopg2-binary` con consultas parametrizadas para prevenir inyecciones SQL.
  * Manejo de credenciales mediante variables de entorno (`.env`).

---

##  Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Base de Datos:** PostgreSQL
* **Librerías principales:**
  * `psycopg2-binary`: Conector para PostgreSQL.
  * `python-dotenv`: Manejo seguro de variables de entorno.

---

## Estructura del Proyecto

```text
Supermarket/
│
├── database/
│   ├── __init__.py
│   └── db_manager.py         # Conexión y gestión de PostgreSQL
│
├── moduls/
│   ├── __init__.py
│   ├── usuario.py            # Modelo POO de Usuario
│   └── producto.py           # Modelo POO de Producto
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py       # Lógica de registro e inicio de sesión
│   └── inventario_service.py # CRUD de productos en PostgreSQL
│
├── ui/
│   ├── __init__.py
│   └── menu.py               # Menú interactivo por consola
│
├── .env                      # Variables de entorno (no subir a Git)
├── .gitignore
├── main.py                   # Punto de entrada de la aplicación
├── README.md                 # Documentación del repositorio
├── test_auth.py              # Script de prueba del servicio de autenticación
└── test_inventario.py        # Script de prueba del servicio de inventario
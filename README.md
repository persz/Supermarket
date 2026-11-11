# Supermarket - Sistema de Gestión y Facturación Automática

Aplicación modular en Python para la gestión de un supermercado virtual, desarrollada bajo el paradigma de **Programación Orientada a Objetos (POO)** e integrada con una base de datos relacional **PostgreSQL**, generación de facturas en **PDF** y envío automático de recibos por **correo electrónico (SMTP)**.

---

## Características Principales

* **Autenticación y Control de Roles:**
  * Registro e inicio de sesión seguro de usuarios.
  * Roles diferenciados: `admin` (gestión completa de existencias) y `cliente` (catálogo y carrito).
* **Gestión de Inventario (CRUD):**
  * Alta, consulta, actualización de stock y eliminación de productos en PostgreSQL.
* **Carrito de Compras y Ventas:**
  * Gestión en memoria del carrito por cliente con control en tiempo real del stock disponible.
  * Registro transaccional de ventas y detalle de productos (`ventas` y `detalle_ventas`).
* **Facturación PDF y Envío Automático por Email:**
  * Generación dinámica de facturas en formato PDF con `ReportLab`.
  * Envío automático del recibo adjunto al correo electrónico registrado del cliente mediante `smtplib` (Gmail SMTP).

---

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Base de Datos:** PostgreSQL
* **Librerías Principales:**
  * `psycopg2-binary`: Conector relacional para PostgreSQL.
  * `reportlab`: Generación y diseño de documentos PDF.
  * `python-dotenv`: Manejo seguro de credenciales y variables de entorno.
  * `smtplib` / `email`: Servicio integrado para comunicación por correo electrónico.

---

## Estructura del Proyecto

```text
Supermarket/
├── database/
│   ├── __init__.py
│   └── db_manager.py
├── facturas/
├── moduls/
│   ├── __init__.py
│   ├── usuario.py
│   ├── producto.py
│   └── venta.py
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── inventario_service.py
│   ├── venta_service.py
│   └── email_service.py
├── ui/
│   ├── __init__.py
│   └── menu.py
├── .env
├── .gitignore
├── main.py
└── README.md         
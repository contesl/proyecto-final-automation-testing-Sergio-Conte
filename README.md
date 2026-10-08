# Proyecto Final - Framework de Automatización de Pruebas (UI y API)

Framework de automatización de pruebas híbrido desarrollado en Python, diseñado para evaluar tanto interfaces web (UI) mediante **Selenium WebDriver** como servicios web (API) mediante la biblioteca **Requests**. El proyecto implementa el patrón de diseño **Page Object Model (POM)** para garantizar un código modular, mantenible y escalable.

## 🚀 Tecnologías Utilizadas

- **Lenguaje:** Python 3.13+
- **Framework de Testing:** Pytest
- **Automatización UI:** Selenium WebDriver
- **Pruebas de API:** Requests
- **Patrón de Diseño:** Page Object Model (POM)
- **Gestión de Reportes:** Pytest HTML Reports
- **Control de Versiones:** Git y GitHub

## 📂 Estructura del Proyecto

```
proyecto-final-automation-testing-Sergio-Conte/
│
├── pages/                  # Clases del Patrón Page Object Model (UI)
│   ├── base_page.py        # Métodos genéricos y esperas explícitas de Selenium
│   ├── login_page.py       # Interacciones con la vista de Login
│   ├── inventory_page.py   # Interacciones con el catálogo de productos
│   ├── cart_page.py        # Gestión del carrito de compras
│   └── checkout_page.py    # Flujo de pago y confirmación de compra
│
├── tests/                  # Casos de prueba automatizados
│   ├── test_ui_saucedemo.py # Pruebas End-to-End de la interfaz web
│   └── test_api_reqres.py  # Pruebas de integración de la API (ReqRes)
│
├── utils/                  # Archivos de configuración y datos externos
│   └── usuarios.json       # Datos de prueba parametrizados (Credenciales, Checkout)
│
├── reports/                # Directorio de salida para capturas de pantalla y reportes HTML
├── conftest.py             # Fixtures globales (inicialización de drivers y hooks de fallos)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación general del proyecto
```

## ⚙️ ¿Cómo instalar las dependencias?

1. Clona el repositorio y abre una terminal en la carpeta raíz del proyecto.

2. Crea y activa un entorno virtual de Python:

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate
```

3. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ ¿Cómo ejecutar las pruebas?

- **Todas las pruebas:** `python -m pytest -v`
- **Pruebas de UI (SauceDemo):** `python -m pytest tests/test_ui_saucedemo.py -v`
- **Pruebas de API (ReqRes):** `python -m pytest tests/test_api_reqres.py -v`
- **Con reporte HTML:** `python -m pytest -v --html=reports/reporte.html --self-contained-html`

## 🧪 Casos de Prueba

### UI — SauceDemo (`test_ui_saucedemo.py`)

Los tests cubren flujos completos sobre [saucedemo.com](https://www.saucedemo.com), utilizando datos parametrizados desde `utils/usuarios.json`.

| # | Nombre | Descripción |
|---|--------|-------------|
| 01 | `test_01_login_exitoso` | Verifica el acceso exitoso con credenciales válidas. Valida URL e título de inventario. |
| 02 | `test_02_login_fallido_escenario_negativo` | **Escenario negativo.** Intenta ingresar con usuario bloqueado (`locked_out_user`) y valida el mensaje de error esperado. |
| 03 | `test_03_verificacion_catalogo_e_interfaz` | Valida que la pantalla de catálogo cargue correctamente: menú, filtro y datos del primer producto. |
| 04 | `test_04_agregar_producto_al_carrito` | Agrega el primer producto al carrito y verifica el badge y el contenido del carrito. |
| 05 | `test_05_flujo_completo_checkout` | Flujo End-to-End completo: login → agregar producto → carrito → checkout → confirmación. |

### API — ReqRes (`test_api_reqres.py`)

Los tests cubren la API pública [reqres.in](https://reqres.in), validando estructura y contenido de respuestas JSON.

| # | Nombre | Método | Endpoint | Validaciones |
|---|--------|--------|----------|--------------|
| 01 | `test_api_get_users` | GET | `/api/users?page=2` | Status 200, campo `data` presente y no vacío. |
| 02 | `test_api_create_user` | POST | `/api/users` | Status 201, `name` y `job` coinciden con payload, `id` generado. |
| 03 | `test_api_delete_user` | DELETE | `/api/users/2` | Status 204 sin contenido. |

## 📋 Datos de Prueba Parametrizados

Los datos de prueba se gestionan desde `utils/usuarios.json`, separando la lógica de los tests de los valores concretos:

```json
{
  "usuario_valido": {
    "username": "standard_user",
    "password": "secret_sauce"
  },
  "usuario_bloqueado": {
    "username": "locked_out_user",
    "password": "secret_sauce",
    "mensaje_error": "Epic sadface: Sorry, this user has been locked out."
  },
  "datos_checkout": {
    "nombre": "Sergio",
    "apellido": "Conte",
    "codigo_postal": "1000"
  }
}
```

Para agregar nuevos conjuntos de datos, basta con extender el archivo JSON sin modificar el código de los tests.

## 📊 ¿Cómo interpretar los reportes generados?

1. **Logs en consola:** Registro detallado en tiempo real de los pasos clave y estados de cada test.
2. **Capturas de pantalla automáticas:** Si una prueba de UI falla, se guarda automáticamente una evidencia en `.png` dentro de `reports/`, con nombre descriptivo que incluye fecha/hora y nombre del test.
3. **Reportes HTML:** Resumen detallado con estado (Passed/Failed), duración de cada prueba y capturas embebidas para los casos fallidos.

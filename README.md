# Proyecto Final - Framework de Automatización de Pruebas (UI y API)

Framework de automatización de pruebas híbrido desarrollado en Python, diseñado para evaluar tanto interfaces web (UI) mediante **Selenium WebDriver** como servicios web (API) mediante la biblioteca **Requests**. El proyecto implementa el patrón de diseño **Page Object Model (POM)** para garantizar un código modular, mantenible y escalable.

## 🎯 Propósito del Proyecto

Demostrar un framework de testing automatizado completo que:

- Automatiza flujos reales de un sitio web de práctica ([saucedemo.com](https://www.saucedemo.com)), incluyendo escenarios positivos y negativos.
- Valida una API REST pública ([reqres.in](https://reqres.in)) con distintos métodos HTTP, casos de éxito y de error.
- Separa los datos de prueba del código y los ejecuta de forma parametrizada.
- Genera reportes HTML, logs detallados y capturas de pantalla automáticas cuando una prueba falla.
- Se ejecuta automáticamente en cada `push` mediante GitHub Actions.

## 🚀 Tecnologías Utilizadas

- **Lenguaje:** Python 3.13+
- **Framework de Testing:** Pytest
- **Automatización UI:** Selenium WebDriver
- **Pruebas de API:** Requests
- **Patrón de Diseño:** Page Object Model (POM)
- **Reportes:** pytest-html
- **Control de Versiones:** Git y GitHub
- **CI/CD:** GitHub Actions

## 📂 Estructura del Proyecto

```
proyecto-final-automation-testing-Sergio-Conte/
│
├── pages/                    # Clases del patrón Page Object Model (UI)
│   ├── base_page.py          # Métodos genéricos, esperas explícitas y logging de acciones
│   ├── login_page.py         # Interacciones con la vista de Login
│   ├── inventory_page.py     # Interacciones con el catálogo de productos
│   ├── cart_page.py          # Gestión del carrito de compras
│   └── checkout_page.py      # Flujo de pago y confirmación de compra
│
├── tests/                    # Casos de prueba automatizados
│   ├── conftest.py           # Fixture del navegador + hook de capturas en fallos
│   ├── test_ui_saucedemo.py  # Pruebas End-to-End de la interfaz web
│   └── test_api_reqres.py    # Pruebas de la API (ReqRes)
│
├── datos/
│   └── usuarios.json         # Datos de prueba externos (usuarios válidos/inválidos, checkout)
│
├── utils/
│   └── logger.py             # Configuración del sistema de logging (archivo + consola)
│
├── .github/workflows/
│   └── tests.yml             # Pipeline de CI/CD con GitHub Actions
│
├── reports/                  # Se genera al ejecutar: reporte HTML, log y capturas (no se versiona)
├── pytest.ini                # Configuración de Pytest (reporte HTML por defecto)
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación del proyecto
```

## ⚙️ ¿Cómo instalar las dependencias?

**Requisitos previos:** Python 3.13+ y Google Chrome instalados. Selenium descarga automáticamente el driver compatible con tu versión de Chrome.

1. Clona el repositorio y abre una terminal en la carpeta raíz del proyecto:

```bash
git clone https://github.com/contesl/proyecto-final-automation-testing-Sergio-Conte.git
cd proyecto-final-automation-testing-Sergio-Conte
```

2. Crea y activa un entorno virtual de Python:

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux / macOS:
source venv/bin/activate
```

3. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ ¿Cómo ejecutar las pruebas?

Gracias a `pytest.ini`, cada ejecución genera automáticamente el reporte HTML en `reports/reporte.html`.

- **Todas las pruebas:** `python -m pytest`
- **Solo pruebas de UI (SauceDemo):** `python -m pytest tests/test_ui_saucedemo.py`
- **Solo pruebas de API (ReqRes):** `python -m pytest tests/test_api_reqres.py`
- **Un caso puntual:** `python -m pytest -k "login_fallido"`

> Las pruebas de UI se ejecutan en modo *headless* (sin abrir la ventana del navegador). Para ver el navegador mientras corre, comentá la línea `--headless=new` en `tests/conftest.py`.

## 🧪 Casos de Prueba

### UI — SauceDemo (`test_ui_saucedemo.py`)

| # | Nombre | Descripción |
|---|--------|-------------|
| 01 | `test_01_login_exitoso` | **Parametrizado.** Se ejecuta una vez por cada usuario de `usuarios_validos` y verifica URL y título del inventario. |
| 02 | `test_02_login_fallido_escenario_negativo` | **Escenario negativo parametrizado.** Se ejecuta por cada caso de `usuarios_invalidos` (usuario bloqueado, password incorrecta, usuario vacío, password vacía) y valida el mensaje de error y que no se ingrese al sistema. |
| 03 | `test_03_verificacion_catalogo_e_interfaz` | Valida que el catálogo cargue correctamente: menú, filtro y nombre/precio del primer producto. |
| 04 | `test_04_agregar_producto_al_carrito` | Agrega el primer producto al carrito y verifica el contador y el contenido del carrito. |
| 05 | `test_05_flujo_completo_checkout` | Flujo End-to-End completo: login → agregar producto → carrito → checkout → confirmación. |

### API — ReqRes (`test_api_reqres.py`)

| # | Nombre | Método | Endpoint | Escenario | Validaciones |
|---|--------|--------|----------|-----------|--------------|
| 01 | `test_api_get_users` | GET | `/api/users?page=2` | Éxito | Status 200, página correcta, cada usuario con `id`, `email`, `first_name`, `last_name`, `avatar`. |
| 02 | `test_api_create_user` | POST | `/api/users` | Éxito | Status 201, `name` y `job` coinciden con el payload, `id` y `createdAt` generados. |
| 03 | `test_api_delete_user` | DELETE | `/api/users/2` | Éxito | Status 204 sin contenido. |
| 04 | `test_api_get_usuario_inexistente` | GET | `/api/users/23` | Error | Status 404 y cuerpo JSON vacío. |
| 05 | `test_api_login_sin_password` | POST | `/api/login` | Error | Status 400 y mensaje `{"error": "Missing password"}`. |

## 📋 Datos de Prueba Parametrizados

Los datos se leen desde `datos/usuarios.json`, separando la lógica de los tests de los valores concretos. Los tests 01 y 02 usan `@pytest.mark.parametrize`, así que **cada elemento de la lista es una ejecución independiente** que aparece por separado en el reporte (por ejemplo `test_02_login_fallido_escenario_negativo[password_vacia]`).

```json
{
  "usuarios_validos": [
    { "username": "standard_user", "password": "secret_sauce" }
  ],
  "usuarios_invalidos": [
    {
      "caso": "usuario_bloqueado",
      "username": "locked_out_user",
      "password": "secret_sauce",
      "mensaje_error": "Epic sadface: Sorry, this user has been locked out."
    }
  ],
  "datos_checkout": { "nombre": "Sergio", "apellido": "Conte", "codigo_postal": "1000" }
}
```

Para agregar un nuevo caso, basta con sumar un elemento a la lista correspondiente del JSON, sin modificar el código de los tests.

## ⚡ Integración Continua con GitHub Actions

El pipeline definido en `.github/workflows/tests.yml` se ejecuta automáticamente en cada `push` o `pull request` a la rama `main`:

1. Levanta una máquina virtual Ubuntu limpia.
2. Instala Python 3.13 y las dependencias del proyecto (con caché para mayor velocidad).
3. Ejecuta las pruebas de API y genera `reporte_api.html`.
4. Ejecuta las pruebas de UI en modo headless y genera `reporte_ui.html`.
5. Sube los reportes, el log y las capturas como artefactos descargables (aunque alguna prueba falle).

**¿Cómo ver los resultados?** Entrá a la pestaña **Actions** del repositorio, elegí la ejecución más reciente y descargá `test-reports` desde la sección **Artifacts** (disponible por 30 días).

## 📊 ¿Cómo interpretar los reportes generados?

Después de cada ejecución, la carpeta `reports/` contiene:

1. **`reporte.html` — Reporte HTML.** Abrilo con cualquier navegador. Arriba muestra el resumen (cantidad de tests *Passed*, *Failed*, *Skipped* y duración total) y debajo una tabla con cada test, su estado y su duración. Al expandir un test fallido se ve el error de Python (qué *assert* falló y en qué línea) y **la captura de pantalla del navegador en el momento del fallo**.
2. **`execution.log` — Log de ejecución.** Registro con fecha y hora de cada paso clave: apertura del navegador, URLs visitadas, clics, campos completados, textos leídos, peticiones a la API con su código de respuesta y el resultado (*PASSED* / *FAILED*) de cada test. Es el primer lugar donde mirar para entender en qué paso se rompió una prueba. Por seguridad, el log registra el nombre de los campos pero no los valores escritos (ej. contraseñas).
3. **`screenshots/` — Capturas de fallos.** Solo se generan cuando una prueba de UI falla. El nombre incluye el test y la fecha/hora, por ejemplo: `test_05_flujo_completo_checkout_2026-11-05_14-32-10.png`.

> Si todos los tests pasan, la carpeta `screenshots/` no se crea: es la señal de que no hubo fallos de UI.

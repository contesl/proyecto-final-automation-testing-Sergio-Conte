# Proyecto Final - Framework de Automatización de Pruebas (UI y API)

Framework de automatización de pruebas desarrollado en **Python** que prueba de forma automática:

- **Una página web** ([saucedemo.com](https://www.saucedemo.com), una tienda online de práctica), usando **Selenium WebDriver**.
- **Una API** ([reqres.in](https://reqres.in), un servicio público de práctica), usando la biblioteca **Requests**.

## 🎯 ¿Qué hace este proyecto?

En lugar de que una persona abra el navegador y pruebe la tienda a mano (iniciar sesión, agregar un producto, comprar...), este proyecto lo hace **solo**: abre Chrome, hace los clics, completa los formularios y verifica que todo funcione como se espera. Lo mismo con la API: envía pedidos y controla que las respuestas sean correctas.

Al terminar, genera:

- Un **reporte HTML** con el resultado de cada prueba (pasó / falló) y cuánto tardó.
- Un **log** (registro) con todos los pasos que se hicieron.
- **Capturas de pantalla** automáticas de las pruebas que fallan, para ver qué pasó.

Además, cada vez que se sube código a GitHub, las pruebas se ejecutan solas en la nube (**GitHub Actions**).

## 📖 Glosario rápido

| Término | Qué significa |
|---------|---------------|
| **Test / prueba / caso de prueba** | Un chequeo automático: hace algo y verifica el resultado. |
| **UI** | *User Interface*: la parte visual de la página web (botones, formularios). |
| **API** | Un servicio que intercambia datos entre programas, sin pantalla. |
| **Selenium** | Herramienta que controla el navegador como si fuera una persona. |
| **Pytest** | Herramienta que ejecuta los tests y muestra los resultados. |
| **Page Object Model (POM)** | Forma de organizar el código: cada pantalla del sitio tiene su propia clase con sus acciones (ej. `LoginPage.login()`). Si la página cambia, se corrige en un solo lugar. |
| **Parametrización** | Ejecutar el mismo test varias veces con datos distintos (ej. varios usuarios). |
| **Headless** | El navegador se abre "invisible", sin mostrar la ventana. |
| **Assert** | La línea del test que verifica algo. Si no se cumple, el test falla. |
| **CI/CD (GitHub Actions)** | Ejecución automática de las pruebas en GitHub cada vez que se sube código. |

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
├── pages/                    # Una clase por cada pantalla del sitio (Page Object Model)
│   ├── base_page.py          # Acciones comunes a todas las pantallas (clic, escribir, leer)
│   ├── login_page.py         # Pantalla de inicio de sesión
│   ├── inventory_page.py     # Catálogo de productos
│   ├── cart_page.py          # Carrito de compras
│   ├── checkout_information_page.py  # Checkout paso 1: datos del comprador
│   ├── checkout_overview_page.py     # Checkout paso 2: resumen de la orden
│   └── checkout_complete_page.py     # Checkout paso 3: confirmación de la compra
│
├── tests/                    # Las pruebas automatizadas
│   ├── conftest.py           # Abre/cierra Chrome en cada test y toma capturas si falla
│   ├── test_ui_saucedemo.py  # Pruebas de la página web
│   └── test_api_reqres.py    # Pruebas de la API
│
├── datos/
│   └── usuarios.json         # Datos de prueba: usuarios válidos, inválidos y datos de compra
│
├── utils/
│   └── logger.py             # Configuración del log (registro de pasos)
│
├── .github/workflows/
│   └── tests.yml             # Instrucciones para que GitHub ejecute las pruebas solo
│
├── reports/                  # Se crea al ejecutar las pruebas (reporte, log y capturas). No se sube a GitHub
├── pytest.ini                # Configuración de Pytest
├── requirements.txt          # Lista de librerías que necesita el proyecto
└── README.md                 # Este archivo
```

## ⚙️ ¿Cómo instalar las dependencias?

### Antes de empezar, necesitás tener instalado:

1. **Python 3.13 o superior** → [python.org/downloads](https://www.python.org/downloads/)
   - En Windows, durante la instalación **tildá la opción "Add Python to PATH"**.
   - Para verificar que quedó instalado, abrí una terminal y escribí `python --version`. Tiene que mostrar algo como `Python 3.13.2`.
2. **Google Chrome** → [google.com/chrome](https://www.google.com/chrome/)
3. **Git** (para descargar el proyecto) → [git-scm.com](https://git-scm.com/downloads)

> No hace falta descargar el "ChromeDriver": Selenium lo descarga solo, en la versión que corresponda a tu Chrome.

### Paso a paso

**1. Descargar el proyecto** y entrar a su carpeta:

```bash
git clone https://github.com/contesl/proyecto-final-automation-testing-Sergio-Conte.git
cd proyecto-final-automation-testing-Sergio-Conte
```

**2. Crear un entorno virtual** (recomendado). Es una "caja" separada donde se instalan las librerías del proyecto sin mezclarse con otras de la PC:

```bash
python -m venv venv
```

Y activarlo:

```bash
# En Windows:
venv\Scripts\activate

# En Linux / macOS:
source venv/bin/activate
```

Si se activó bien, al principio de la línea de la terminal aparece `(venv)`.

**3. Instalar las librerías** del proyecto:

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ ¿Cómo ejecutar las pruebas?

Siempre desde la carpeta raíz del proyecto (la que contiene `pytest.ini`):

| Quiero ejecutar... | Comando |
|--------------------|---------|
| **Todas las pruebas** | `python -m pytest` |
| Solo las pruebas de la página web | `python -m pytest tests/test_ui_saucedemo.py` |
| Solo las pruebas de la API | `python -m pytest tests/test_api_reqres.py` |
| Solo las pruebas cuyo nombre contenga una palabra | `python -m pytest -k "login"` |

### ¿Qué voy a ver?

Mientras corren, la terminal muestra cada paso (abrir la página, clics, respuestas de la API) y el resultado de cada prueba. Al final aparece un resumen como este:

```
tests/test_api_reqres.py::test_api_get_users PASSED                      [  7%]
...
tests/test_ui_saucedemo.py::test_05_flujo_completo_checkout PASSED       [100%]

- Generated html report: file:///.../reports/reporte.html -
============================ 15 passed in 100.53s =============================
```

- `PASSED` (en verde) = la prueba funcionó.
- `FAILED` (en rojo) = algo no dio el resultado esperado.
- `ERROR` = la prueba ni siquiera pudo empezar (por ejemplo, no se pudo abrir Chrome).

La ejecución completa tarda entre 1 y 3 minutos, según la conexión a internet.

> **¿Querés ver el navegador mientras trabaja?** Las pruebas corren en modo *headless* (Chrome invisible). Para verlo, en `tests/conftest.py` poné un `#` al principio de la línea `options.add_argument("--headless=new")`. Acordate de sacarlo antes de subir los cambios: GitHub Actions necesita el modo headless.

## 🧪 Casos de Prueba

### Página web — SauceDemo (`test_ui_saucedemo.py`)

| # | Prueba | ¿Qué verifica? |
|---|--------|----------------|
| 01 | `test_01_login_exitoso` | Que se pueda iniciar sesión y se llegue al catálogo de productos. **Se ejecuta una vez por cada usuario válido** del archivo de datos. |
| 02 | `test_02_login_fallido_escenario_negativo` | **Escenario negativo:** que con datos incorrectos NO se pueda entrar y aparezca el mensaje de error correcto. Se ejecuta con 4 casos: usuario bloqueado, contraseña incorrecta, usuario vacío y contraseña vacía. |
| 03 | `test_03_verificacion_catalogo_e_interfaz` | Que el catálogo cargue bien: menú, filtro y nombre/precio del primer producto. |
| 04 | `test_04_agregar_producto_al_carrito` | Que al agregar un producto, el contador del carrito muestre 1 y el producto aparezca en el carrito. |
| 05 | `test_05_flujo_completo_checkout` | Una compra completa de principio a fin: login → agregar producto → carrito → datos del comprador → resumen (verifica producto y total) → confirmación. |

### API — ReqRes (`test_api_reqres.py`)

| # | Prueba | Método | Endpoint | Tipo | ¿Qué verifica? |
|---|--------|--------|----------|------|----------------|
| 01 | `test_api_get_users` | GET | `/api/users?page=2` | Éxito | Respuesta 200, página correcta y que cada usuario tenga `id`, `email`, `first_name`, `last_name` y `avatar`. |
| 02 | `test_api_create_user` | POST | `/api/users` | Éxito | Respuesta 201 y que devuelva los datos enviados, con `id` y fecha de creación. |
| 03 | `test_api_delete_user` | DELETE | `/api/users/2` | Éxito | Respuesta 204, sin contenido. |
| 04 | `test_api_get_usuario_inexistente` | GET | `/api/users/23` | Error | Respuesta 404 (no encontrado) y cuerpo vacío. |
| 05 | `test_api_login_sin_password` | POST | `/api/login` | Error | Respuesta 400 y el mensaje `Missing password`. |
| 06 | `test_api_flujo_encadenado_listar_y_consultar_usuario` | GET + GET | `/api/users?page=2` → `/api/users/{id}` | Encadenado | Toma el `id` del primer usuario de la lista y lo consulta individualmente: los datos deben coincidir en ambas respuestas. |

**¿Qué es una petición encadenada?** Una petición que usa un dato obtenido en la respuesta de otra. En el caso 06, el `id` que se consulta no está escrito en el código: sale de la primera respuesta.

**¿Qué son esos números?** Son los *códigos de estado HTTP* que devuelve la API: `200` = OK, `201` = creado, `204` = eliminado sin contenido, `400` = pedido incorrecto, `404` = no encontrado.

## 📋 Datos de Prueba

Los usuarios, contraseñas y datos del comprador **no están escritos dentro de los tests**: se leen del archivo `datos/usuarios.json`. Así, para probar con otros datos no hace falta tocar el código.

Ejemplo de cómo está organizado:

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

**Para agregar un caso nuevo**, alcanza con sumar un elemento a la lista que corresponda. Por ejemplo, un nuevo usuario inválido dentro de `usuarios_invalidos`. La próxima vez que se ejecuten las pruebas, aparecerá como un test más en el reporte (por ejemplo `test_02_login_fallido_escenario_negativo[mi_caso_nuevo]`).

## ⚡ Ejecución automática en GitHub (GitHub Actions)

Cada vez que se sube código a la rama `main` (o se abre un *pull request*), GitHub ejecuta las pruebas solo, siguiendo las instrucciones de `.github/workflows/tests.yml`:

1. Prepara una máquina virtual Linux limpia.
2. Instala Python y las librerías del proyecto.
3. Ejecuta las pruebas de API y luego las de la página web.
4. Guarda los reportes, el log y las capturas para descargarlos.

**¿Cómo ver los resultados?**

1. Entrá al repositorio en GitHub y hacé clic en la pestaña **Actions**.
2. Elegí la ejecución más reciente: ✅ verde = todo pasó, ❌ roja = algo falló.
3. Abajo de todo, en la sección **Artifacts**, descargá `test-reports` (un .zip con los reportes). Queda disponible 30 días.

## 📊 ¿Cómo interpretar los reportes generados?

Después de cada ejecución se crea la carpeta `reports/` con estos archivos:

### 1. `reporte.html` — el reporte principal

Abrilo con doble clic (se abre en el navegador).

- **Arriba:** el resumen. Cuántas pruebas pasaron (*Passed*), fallaron (*Failed*) o no pudieron ejecutarse (*Errors*), y cuánto tardó todo.
- **Abajo:** una tabla con cada prueba, su resultado y su duración. Se puede filtrar haciendo clic en los contadores del resumen.
- **Si una prueba falló:** hacé clic sobre ella para ver el detalle. Vas a ver el error (qué verificación no se cumplió y en qué línea del código) y **la captura de pantalla del navegador en el momento del fallo**.

### 2. `execution.log` — el registro paso a paso

Se abre con cualquier editor de texto. Cada línea tiene fecha, hora y lo que se hizo:

```
2026-11-05 09:04:56 - [INFO] - Iniciando sesión con el usuario: 'standard_user'
2026-11-05 09:04:56 - [INFO] - Click en: login-button
2026-11-05 09:05:30 - [INFO] - Resultado de test_04_agregar_producto_al_carrito: FAILED (37.44s)
```

Sirve para encontrar **en qué paso exacto** se rompió una prueba: el problema suele estar justo después del último paso que aparece antes del `FAILED`. Por seguridad, el log muestra en qué campo se escribió, pero no lo que se escribió (para no dejar contraseñas).

### 3. `screenshots/` — capturas de las pruebas que fallaron

Solo se crea si alguna prueba de la página web falla. Cada imagen lleva el nombre de la prueba y la fecha/hora, por ejemplo:

`test_05_flujo_completo_checkout_2026-11-05_14-32-10.png`

> Si esta carpeta no existe después de ejecutar, ¡buena señal! Significa que no falló ninguna prueba de la página web.

## 🛠️ Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `'python' no se reconoce como un comando` | Python no está instalado o no se agregó al PATH. Reinstalalo tildando **"Add Python to PATH"**. |
| `No module named 'selenium'` (o `pytest`, `requests`) | Faltan las librerías. Ejecutá `pip install -r requirements.txt` (con el entorno virtual activado, si lo usás). |
| `file or directory not found: tests` | Estás en otra carpeta. Entrá con `cd` a la carpeta del proyecto (la que tiene `pytest.ini`). |
| `SessionNotCreatedException` / `DevToolsActivePort file doesn't exist` | Chrome no pudo abrirse. Verificá que Chrome esté instalado y actualizado. Si persiste, cerrá todas las ventanas de Chrome y volvé a ejecutar. |
| Las pruebas de API fallan por `Timeout` | La API tardó demasiado en responder (más de 30 segundos). Revisá tu conexión a internet y volvé a intentar. |
| La primera prueba tarda mucho en arrancar | Es normal: la primera vez Selenium descarga el driver de Chrome y la primera llamada a la API puede demorar unos segundos. |

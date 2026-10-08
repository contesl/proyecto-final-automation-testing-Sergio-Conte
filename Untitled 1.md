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

Plaintext

```
`proyecto-final-automation-testing-Sergio-Conte/`

`│`

`├── pages/                  \# Clases del Patrón Page Object Model (UI)`

`│   ├── base\_page.py        \# Métodos genéricos y esperas explícitas de Selenium`

`│   ├── login\_page.py       \# Interacciones con la vista de Login`

`│   ├── inventory\_page.py   \# Interacciones con el catálogo de productos`

`│   ├── cart\_page.py        \# Gestión del carrito de compras`

`│   └── checkout\_page.py    \# Flujo de pago y confirmación de compra`

`│`

`├── tests/                  \# Casos de prueba automatizados`

`│   ├── test\_ui\_saucedemo.py\# Pruebas End-to-End de la interfaz web`

`│   └── test\_api\_reqres.py  \# Pruebas de integración de la API (ReqRes)`

`│`

`├── utils/                  \# Archivos de configuración y datos externos`

`│   └── usuarios.json       \# Datos de prueba parametrizados (Credenciales, Checkout)`

`│`

`├── reports/                \# Directorio de salida para capturas de pantalla y reportes HTML`

`├── conftest.py             \# Fixtures globales (inicialización de drivers y hooks de fallos)`

`├── requirements.txt        \# Dependencias del proyecto`

`└── README.md               \# Documentación general del proyecto`
```

## ⚙️ ¿Cómo instalar las dependencias?

1. Clona el repositorio y abre una terminal en la carpeta raíz del proyecto.

2. Crea y activa un entorno virtual de Python:

Bash

```
`python -m venv venv`

`\# En Windows:`

`venv\\Scripts\\activate`
```

3. Instala las dependencias necesarias:

Bash

```
`pip install -r requirements.txt`
```

## 🏃♂️ ¿Cómo ejecutar las pruebas?

- **Todas las pruebas:** `python -m pytest -v`

- **Pruebas de UI (SauceDemo):** `python -m pytest tests/test\_ui\_saucedemo.py -v`

- **Pruebas de API (ReqRes):** `python -m pytest tests/test\_api\_reqres.py -v`

## 📊 ¿Cómo interpretar los reportes generados?

\[cite: 5\] 

1. **Logs en consola:** Registro detallado en tiempo real de los pasos clave y estados\[cite: 5\].

2. **Capturas de pantalla automáticas:** Si una prueba de UI falla, se guarda una evidencia en `.png` dentro de la carpeta `reports/`\[cite: 5\].

3. **Reportes HTML:** Resumen detallado con estados (Passed/Failed) y duración de las pruebas\[cite: 5\].


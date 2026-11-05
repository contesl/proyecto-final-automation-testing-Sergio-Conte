"""
conftest.py
-----------
Configuración compartida por todos los tests. Pytest lee este archivo
automáticamente antes de ejecutar las pruebas.

Contiene:
  - El fixture 'driver': abre un navegador Chrome nuevo para cada test de UI
    y lo cierra al terminar (así cada test es independiente de los demás).
  - El hook 'pytest_runtest_makereport': registra el resultado de cada test y,
    si un test de UI falla, guarda una captura de pantalla y la agrega al
    reporte HTML.
"""

import os
import re
import shutil
import tempfile
from datetime import datetime

import pytest
from selenium import webdriver
from utils.logger import setup_logger

# Logger del proyecto (escribe en reports/execution.log y en la terminal)
logger = setup_logger()

# Carpeta donde se guardan las capturas de pantalla de los tests que fallan
SCREENSHOTS_DIR = os.path.join(os.getcwd(), "reports", "screenshots")


@pytest.fixture
def driver(request):
    """
    Fixture que prepara el navegador para un test de UI.

    Un "fixture" es una función que Pytest ejecuta automáticamente antes de
    cada test que lo pida como parámetro (por ejemplo: def test_x(driver)).
      1. Antes del test: configura y abre Chrome.
      2. Durante el test: entrega el navegador (yield).
      3. Después del test: cierra Chrome y limpia, haya pasado o fallado.
    """
    logger.info(f"Iniciando navegador Chrome para: {request.node.name}")
    options = webdriver.ChromeOptions()

    # Perfil de Chrome temporal y exclusivo para cada test. Evita conflictos con
    # un Chrome que ya esté abierto en la PC o con un perfil bloqueado
    # (error "DevToolsActivePort file doesn't exist")
    perfil_temporal = tempfile.mkdtemp(prefix="chrome_test_")
    options.add_argument(f"--user-data-dir={perfil_temporal}")

    options.add_argument("--no-sandbox")             # Necesario en entornos de CI/CD o Docker
    options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memoria compartida en Linux
    options.add_argument("--headless=new")            # Ejecuta sin abrir la ventana (modo "headless")
    options.add_argument("--disable-gpu")             # La aceleración gráfica no hace falta
    options.add_argument("--window-size=1920,1080")   # Tamaño de pantalla fijo para todos los tests
    options.add_argument("--disable-extensions")      # Sin extensiones: arranque más rápido y limpio
    options.add_argument("--disable-infobars")        # Oculta barras de aviso del navegador

    # Desactiva el gestor de contraseñas de Chrome. Al loguearse con 'secret_sauce',
    # Chrome detecta que es una contraseña filtrada y muestra el aviso
    # "Cambiá tu contraseña", que toma el foco y bloquea los clics y el tipeo.
    options.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })

    # Abre Chrome con todas las opciones anteriores
    try:
        driver = webdriver.Chrome(options=options)
    except Exception:
        # Si Chrome no puede abrir, se borra el perfil temporal y se informa el error
        logger.error("No se pudo iniciar Chrome.")
        shutil.rmtree(perfil_temporal, ignore_errors=True)
        raise

    # Entrega el navegador al test. El código de abajo se ejecuta cuando el test termina
    yield driver

    # --- Limpieza (teardown): se ejecuta siempre, pase o falle el test ---
    driver.quit()                                       # Cierra el navegador
    shutil.rmtree(perfil_temporal, ignore_errors=True)  # Borra el perfil temporal
    logger.info("Navegador cerrado.")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook que Pytest ejecuta cada vez que genera el resultado de un test.

    Un "hook" es una función con un nombre especial que Pytest llama por su
    cuenta en un momento determinado. Este se usa porque es el único punto
    donde se sabe si el test pasó o falló.
      - Registra en el log el resultado (PASSED / FAILED) y la duración.
      - Si un test de UI falló: guarda una captura con el nombre del test y la
        fecha/hora, y la agrega al reporte HTML.
    """
    # Deja que Pytest arme el resultado y lo obtiene
    outcome = yield
    report = outcome.get_result()

    # Cada test tiene 3 fases: setup (preparación), call (el test) y teardown (limpieza).
    # Solo interesa el resultado de la fase "call"
    if report.when != "call":
        return

    logger.info(f"Resultado de {item.name}: {report.outcome.upper()} ({report.duration:.2f}s)")

    # Si el test pasó, no hace falta captura
    if not report.failed:
        return

    # Solo los tests de UI usan el navegador ('driver'); los de API no tienen pantalla
    driver = item.funcargs.get("driver")
    if driver is None:
        return

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # Nombre del archivo: nombre del test + fecha y hora.
    # Los caracteres que no sirven para un nombre de archivo (como los [ ] de los
    # tests parametrizados) se reemplazan por guiones bajos
    nombre_test = re.sub(r"[^\w\-]", "_", item.name).strip("_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{nombre_test}_{timestamp}.png")

    try:
        driver.save_screenshot(screenshot_path)
        logger.error(f"Test fallido. Captura guardada en: {screenshot_path}")

        # Agrega la captura al reporte HTML (pytest-html), dentro del detalle del test
        pytest_html = item.config.pluginmanager.getplugin("html")
        if pytest_html is not None:
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.png(driver.get_screenshot_as_base64()))
            report.extras = extras
    except Exception as error:
        # Si el navegador ya no responde, se registra el problema sin cortar el resto de los tests
        logger.error(f"No se pudo guardar la captura de pantalla: {error}")

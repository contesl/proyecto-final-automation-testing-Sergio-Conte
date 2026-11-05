import os
import re
from datetime import datetime

import pytest
from selenium import webdriver
from utils.logger import setup_logger

# Inicializa la instancia global del logger
logger = setup_logger()

# Carpeta donde se guardan las capturas de pantalla de los tests fallidos
SCREENSHOTS_DIR = os.path.join(os.getcwd(), "reports", "screenshots")


@pytest.fixture
def driver(request):
    """
    Fixture de Pytest que administra el ciclo de vida del navegador Selenium.
    - Inicializa las opciones de Chrome optimizadas para entornos de CI/CD.
    - Cede el driver al test.
    - Cierra el navegador de forma limpia al finalizar.
    La captura de pantalla en caso de fallo se resuelve en el hook
    pytest_runtest_makereport (más abajo), que es donde Pytest informa
    si el test pasó o falló.
    """
    logger.info(f"Iniciando navegador Chrome para: {request.node.name}")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")             # Necesario para entornos de CI/CD o Docker
    options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memoria compartida
    options.add_argument("--headless=new")            # Ejecución sin ventana gráfica
    options.add_argument("--disable-gpu")             # Deshabilita GPU (innecesaria en CI/CD)
    options.add_argument("--window-size=1920,1080")   # Resolución fija para headless
    options.add_argument("--disable-extensions")      # Desactiva extensiones para mayor velocidad
    options.add_argument("--disable-infobars")        # Elimina barras de información del navegador

    # Instancia el WebDriver de Chrome
    driver = webdriver.Chrome(options=options)

    # Cede el control del driver a la función de prueba que lo invocó
    yield driver

    # --- Teardown: se ejecuta siempre al finalizar cada prueba ---
    driver.quit()
    logger.info("Navegador cerrado.")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de Pytest que se ejecuta al generar el resultado de cada fase del test.
    - Registra en el log el resultado (PASSED / FAILED) y la duración de cada test.
    - Si un test de UI falla, guarda una captura de pantalla con el nombre
      del test y la fecha/hora, y la incrusta en el reporte HTML.
    """
    outcome = yield
    report = outcome.get_result()

    # Solo interesa la fase "call" (la ejecución del test en sí)
    if report.when != "call":
        return

    logger.info(f"Resultado de {item.name}: {report.outcome.upper()} ({report.duration:.2f}s)")

    if not report.failed:
        return

    # Solo los tests de UI usan el fixture 'driver'
    driver = item.funcargs.get("driver")
    if driver is None:
        return

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # Nombre descriptivo: nombre del test + fecha y hora.
    # Se reemplazan caracteres no válidos en nombres de archivo (ej. los [ ] de tests parametrizados)
    nombre_test = re.sub(r"[^\w\-]", "_", item.name).strip("_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{nombre_test}_{timestamp}.png")

    try:
        driver.save_screenshot(screenshot_path)
        logger.error(f"Test fallido. Captura guardada en: {screenshot_path}")

        # Incrusta la captura en el reporte HTML (si pytest-html está activo)
        pytest_html = item.config.pluginmanager.getplugin("html")
        if pytest_html is not None:
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.png(driver.get_screenshot_as_base64()))
            report.extras = extras
    except Exception as error:
        # Si el navegador ya no responde, no se interrumpe el resto de la ejecución
        logger.error(f"No se pudo guardar la captura de pantalla: {error}")

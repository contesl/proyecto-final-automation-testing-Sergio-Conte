import os
import pytest
from selenium import webdriver
from utils.logger import setup_logger

# Inicializa la instancia global del logger
logger = setup_logger()

@pytest.fixture
def driver(request):
    """
    Fixture de Pytest que administra el ciclo de vida del navegador Selenium.
    - Inicializa las opciones de Chrome.
    - Captura screenshots automáticamente al finalizar la ejecución.
    - Cierra el navegador de forma limpia.
    """
    logger.info("Iniciando instancia del navegador Chrome...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")       # Inicia la ventana maximizada
    options.add_argument("--no-sandbox")            # Necesario para entornos de CI/CD o Docker
    options.add_argument("--disable-dev-shm-usage") # Evita problemas de memoria compartida
    options.add_argument("--headless=new")          # Ejecución sin ventana gráfica (ajustable según necesidad)
    
    # Instancia el WebDriver de Chrome
    driver = webdriver.Chrome(options=options)
    
    # Cede el control del driver a la función de prueba que lo invocó
    yield driver

    # --- Bloque de Teardown (Se ejecuta siempre al finalizar cada prueba) ---
    reports_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Genera la captura de pantalla usando el nombre de la prueba
    test_name = request.node.name
    screenshot_path = os.path.join(reports_dir, f"{test_name}.png")
    
    driver.save_screenshot(screenshot_path)
    logger.info(f"Captura de pantalla guardada en: {screenshot_path}")
    
    # Cierra la sesión de Selenium
    driver.quit()
    logger.info("Navegador cerrado.")
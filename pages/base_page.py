"""
base_page.py
------------
Clase base de todos los Page Objects del proyecto.

Reúne las acciones genéricas que se repiten en cualquier pantalla (buscar un
elemento, hacer clic, escribir, leer un texto, verificar si algo está visible).
Las páginas concretas (LoginPage, InventoryPage, etc.) heredan de esta clase,
así no repiten código y todas esperan y registran las acciones de la misma forma.
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger

# Logger compartido: cada acción sobre la página queda registrada en el log
logger = setup_logger()


class BasePage:
    """
    Clase Base que encapsula los métodos genéricos de Selenium WebDriver.

    Todas las acciones usan "esperas explícitas": antes de tocar un elemento,
    se espera (hasta 'timeout' segundos) a que esté listo. Esto evita fallos
    por intentar interactuar con algo que la página todavía no terminó de cargar.

    Los "locators" que reciben los métodos son tuplas con la forma
    (estrategia, valor), por ejemplo: (By.ID, "login-button").
    """

    def __init__(self, driver, timeout=30):
        # driver: el navegador que controla Selenium (lo crea el fixture en conftest.py)
        self.driver = driver
        # wait: objeto que permite "esperar hasta que se cumpla una condición"
        self.wait = WebDriverWait(driver, timeout)

    def get_current_url(self):
        """
        Devuelve la dirección (URL) de la página abierta en el navegador.
        Permite que los tests verifiquen en qué pantalla están sin usar el driver directamente.
        """
        url = self.driver.current_url
        logger.info(f"URL actual: {url}")
        return url

    def find(self, locator):
        """Espera a que un elemento exista en la página (en el DOM) y lo devuelve."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Espera a que un elemento se pueda clickear, lo lleva a la vista y hace clic."""
        logger.info(f"Click en: {locator[1]}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        # Desplaza la página hasta el elemento para asegurar que esté en pantalla
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()

    def send_keys(self, locator, text):
        """Espera un campo de texto, borra lo que tenga y escribe el texto indicado."""
        # Se registra el nombre del campo pero no el valor, para no dejar contraseñas en el log
        logger.info(f"Escribiendo en el campo: {locator[1]}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Espera a que un elemento sea visible y devuelve el texto que muestra."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        texto = element.text
        logger.info(f"Texto leído de {locator[1]}: '{texto}'")
        return texto

    def is_displayed(self, locator):
        """
        Devuelve True si el elemento aparece visible dentro del tiempo de espera,
        o False si no aparece (en lugar de cortar el test con un error).
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except TimeoutException:
            logger.warning(f"Elemento no visible dentro del tiempo de espera: {locator[1]}")
            return False

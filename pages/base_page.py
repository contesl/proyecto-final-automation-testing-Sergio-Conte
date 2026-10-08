from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Clase Base que encapsula todos los métodos genéricos de Selenium WebDriver.
    Aplica el principio de reusabilidad y manejo centralizado de esperas explícitas.
    """
    def __init__(self, driver, timeout=10):
        # Asigna la instancia del navegador y configura una espera explícita predeterminada
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        """Espera explícitamente a que un elemento esté presente en el DOM y lo retorna."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Espera a que un elemento sea interactuable, hace scroll hacia él y realiza un clic."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()

    def send_keys(self, locator, text):
        """Espera el elemento, hace scroll, limpia el contenido y escribe la cadena enviada por parámetro."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Retorna el texto visible de un elemento en pantalla."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element.text

    def is_displayed(self, locator):
        """Comprueba si un elemento es visible en pantalla sin lanzar excepciones si no existe."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except:
            return False
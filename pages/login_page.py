from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """
    Page Object de la página de Login de SauceDemo.
    Almacena los localizadores HTML y encapsula los flujos de inicio de sesión.
    """
    # Mapeo de localizadores (Locators) de los elementos de la interfaz de login
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com"

    def open(self):
        """Abre la URL de la página de inicio de sesión en el navegador."""
        self.driver.get(self.url)

    def login(self, username, password):
        """
        Ejecuta la secuencia completa para iniciar sesión.
        Escribe usuario, contraseña y presiona el botón 'Login'.
        """
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Obtiene el texto del cartel de error en caso de un login fallido."""
        return self.get_text(self.ERROR_MESSAGE)
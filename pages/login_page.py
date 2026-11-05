"""
login_page.py
-------------
Page Object de la pantalla de inicio de sesión de SauceDemo
(https://www.saucedemo.com).

Contiene los localizadores de los campos de usuario, contraseña, botón de
ingreso y mensaje de error, y las acciones que se pueden hacer en esta pantalla.
Los tests llaman a estos métodos en lugar de usar Selenium directamente.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage, logger


class LoginPage(BasePage):
    """Representa la página de Login y sus acciones (abrir, loguearse, leer el error)."""

    # --- Localizadores: cómo encuentra Selenium cada elemento en el HTML ---
    USERNAME_INPUT = (By.ID, "user-name")                    # Campo "Username"
    PASSWORD_INPUT = (By.ID, "password")                     # Campo "Password"
    LOGIN_BUTTON = (By.ID, "login-button")                   # Botón "Login"
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']") # Cartel rojo de error

    def __init__(self, driver):
        super().__init__(driver)
        # Dirección de la página de login
        self.url = "https://www.saucedemo.com"

    def open(self):
        """Abre la página de login en el navegador."""
        logger.info(f"Abriendo página de login: {self.url}")
        self.driver.get(self.url)

    def login(self, username, password):
        """
        Inicia sesión: escribe el usuario, escribe la contraseña y presiona 'Login'.
        Se usa tanto con credenciales válidas como inválidas.
        """
        logger.info(f"Iniciando sesión con el usuario: '{username}'")
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Devuelve el texto del cartel de error que aparece cuando el login falla."""
        return self.get_text(self.ERROR_MESSAGE)

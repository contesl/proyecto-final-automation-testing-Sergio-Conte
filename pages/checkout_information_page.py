"""
checkout_information_page.py
----------------------------
Page Object del paso 1 del checkout: "Checkout: Your Information"
(checkout-step-one.html).

Es el formulario donde el comprador ingresa nombre, apellido y código postal
antes de ver el resumen de la orden.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CheckoutInformationPage(BasePage):
    """Representa el formulario de datos del comprador y sus acciones."""

    # --- Localizadores del formulario ---
    FIRST_NAME_INPUT = (By.ID, "first-name")    # Campo "First Name"
    LAST_NAME_INPUT = (By.ID, "last-name")      # Campo "Last Name"
    POSTAL_CODE_INPUT = (By.ID, "postal-code")  # Campo "Zip/Postal Code"
    CONTINUE_BUTTON = (By.ID, "continue")       # Botón "Continue"

    def fill_information(self, first_name, last_name, postal_code):
        """Completa los tres campos del formulario con los datos recibidos."""
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.POSTAL_CODE_INPUT, postal_code)

    def continue_to_overview(self):
        """
        Presiona 'Continue' y espera a que la URL cambie a 'checkout-step-two.html',
        que confirma que se llegó al resumen de la orden (paso 2).
        """
        self.click(self.CONTINUE_BUTTON)
        self.wait.until(EC.url_contains("checkout-step-two.html"))

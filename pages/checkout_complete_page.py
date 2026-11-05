"""
checkout_complete_page.py
-------------------------
Page Object del paso 3 del checkout: "Checkout: Complete!"
(checkout-complete.html).

Es la pantalla final que confirma que la compra se realizó correctamente.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    """Representa la pantalla de confirmación de la compra."""

    # --- Localizadores de la confirmación ---
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")  # "Thank you for your order!"

    def get_completion_message(self):
        """Devuelve el mensaje de confirmación que aparece al terminar la compra."""
        return self.get_text(self.COMPLETE_HEADER)

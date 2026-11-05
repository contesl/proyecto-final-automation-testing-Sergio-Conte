"""
checkout_overview_page.py
-------------------------
Page Object del paso 2 del checkout: "Checkout: Overview"
(checkout-step-two.html).

Muestra el resumen de la orden (productos, precios y total) y el botón
'Finish' para confirmar la compra.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    """Representa el resumen de la orden y sus acciones."""

    # --- Localizadores del resumen ---
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")  # Nombre del producto en el resumen
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")  # Línea "Total: $..."
    FINISH_BUTTON = (By.ID, "finish")                     # Botón "Finish"

    def get_item_name(self):
        """Devuelve el nombre del (primer) producto que aparece en el resumen de la orden."""
        return self.get_text(self.ITEM_NAME)

    def get_total(self):
        """Devuelve el texto del total de la orden (ej. 'Total: $32.39')."""
        return self.get_text(self.TOTAL_LABEL)

    def finish(self):
        """
        Presiona 'Finish' para confirmar la compra y espera a que la URL cambie a
        'checkout-complete.html' (pantalla de confirmación, paso 3).
        """
        self.click(self.FINISH_BUTTON)
        self.wait.until(EC.url_contains("checkout-complete.html"))

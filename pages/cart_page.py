"""
cart_page.py
------------
Page Object de la pantalla del carrito de compras ("Your Cart").

Permite leer el nombre del producto agregado y avanzar al checkout (pago).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    """Representa el carrito de compras y sus acciones."""

    # --- Localizadores de los elementos del carrito ---
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")  # Nombre del producto en el carrito
    CHECKOUT_BUTTON = (By.ID, "checkout")                # Botón "Checkout"

    def get_item_name(self):
        """Devuelve el nombre del (primer) producto que está en el carrito."""
        return self.get_text(self.ITEM_NAME)

    def proceed_to_checkout(self):
        """
        Presiona 'Checkout' y espera a que la URL cambie a 'checkout-step-one.html',
        que es el formulario con los datos del comprador.
        """
        self.click(self.CHECKOUT_BUTTON)
        self.wait.until(EC.url_contains("checkout-step-one.html"))

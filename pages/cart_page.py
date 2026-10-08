from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Page Object que representa la pantalla del carrito de compras.
    """
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_name(self):
        """Retorna el nombre del primer ítem que se encuentra dentro del carrito."""
        return self.get_text(self.ITEM_NAME)

    def proceed_to_checkout(self):
        """Presiona el botón 'Checkout' para iniciar el proceso de compra."""
        self.click(self.CHECKOUT_BUTTON)
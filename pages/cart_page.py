from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        """
        Presiona el botón 'Checkout' para iniciar el proceso de compra.
        Verifica la navegación mediante la URL resultante, que es más confiable
        que esperar visibilidad de elementos en apps React en entornos de CI/CD.
        """
        self.click(self.CHECKOUT_BUTTON)
        # Confirma la navegación por URL en lugar de visibilidad de elementos
        self.wait.until(EC.url_contains("checkout-step-one.html"))

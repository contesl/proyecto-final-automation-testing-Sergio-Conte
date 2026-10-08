from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Page Object que representa la pantalla del carrito de compras.
    """
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    # Localizador del primer campo del formulario de checkout, utilizado para
    # verificar que la navegación hacia esa pantalla se completó correctamente
    CHECKOUT_FIRST_NAME = (By.ID, "first-name")

    def get_item_name(self):
        """Retorna el nombre del primer ítem que se encuentra dentro del carrito."""
        return self.get_text(self.ITEM_NAME)

    def proceed_to_checkout(self):
        """
        Presiona el botón 'Checkout' para iniciar el proceso de compra.
        Incluye una espera explícita a que el formulario de checkout sea visible
        antes de continuar, evitando condiciones de carrera en entornos de CI/CD.
        """
        self.click(self.CHECKOUT_BUTTON)
        # Espera a que el primer campo del formulario esté disponible como confirmación
        # de que la navegación hacia la pantalla de checkout se completó
        self.wait.until(EC.visibility_of_element_located(self.CHECKOUT_FIRST_NAME))

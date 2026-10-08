from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """
    Page Object de la vista principal del catálogo de productos (Inventory).
    """
    # Localizadores de elementos dentro del catálogo de productos
    TITLE_LABEL = (By.CLASS_NAME, "title")
    FIRST_ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item:nth-child(1) .inventory_item_name")
    FIRST_ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item:nth-child(1) .inventory_item_price")
    FIRST_ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".inventory_item:nth-child(1) button")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    SORT_CONTAINER = (By.CLASS_NAME, "product_sort_container")

    def get_title(self):
        """Retorna el título principal de la sección (ej. 'Products')."""
        return self.get_text(self.TITLE_LABEL)

    def get_first_product_info(self):
        """Obtiene el nombre y el precio del primer producto listado en el catálogo."""
        return self.get_text(self.FIRST_ITEM_NAME), self.get_text(self.FIRST_ITEM_PRICE)

    def add_first_product_to_cart(self):
        """
        Hace clic en el botón 'Add to Cart' del primer producto del catálogo.
        Espera a que el badge del carrito esté presente en el DOM como confirmación
        de que la acción se registró, sin depender de visibilidad de renderizado.
        """
        self.click(self.FIRST_ADD_TO_CART_BTN)
        # Usa presence_of_element_located (más confiable que visibility en apps React)
        self.wait.until(EC.presence_of_element_located(self.CART_BADGE))

    def get_cart_badge_count(self):
        """Obtiene la cantidad de ítems reflejada en la insignia roja del carrito."""
        return self.get_text(self.CART_BADGE)

    def go_to_cart(self):
        """
        Navega hacia la vista del carrito haciendo clic en el ícono del carrito.
        Verifica la navegación mediante la URL resultante, que es más confiable
        que esperar visibilidad de elementos en apps React en entornos de CI/CD.
        """
        self.click(self.CART_LINK)
        # Confirma la navegación por URL en lugar de visibilidad de elementos
        self.wait.until(EC.url_contains("cart.html"))

    def is_interface_loaded(self):
        """Verifica la correcta carga de la interfaz verificando componentes clave."""
        return self.is_displayed(self.MENU_BUTTON) and self.is_displayed(self.SORT_CONTAINER)

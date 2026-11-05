"""
inventory_page.py
-----------------
Page Object de la pantalla principal después del login: el catálogo de
productos ("Products").

Permite leer el título, consultar el primer producto, agregarlo al carrito,
ver el contador del carrito, ir al carrito y comprobar que la interfaz cargó.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Representa el catálogo de productos y sus acciones."""

    # --- Localizadores de los elementos del catálogo ---
    TITLE_LABEL = (By.CLASS_NAME, "title")                    # Título "Products"
    # ".inventory_item:nth-child(1)" = la primera tarjeta de producto de la lista
    FIRST_ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item:nth-child(1) .inventory_item_name")
    FIRST_ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item:nth-child(1) .inventory_item_price")
    FIRST_ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".inventory_item:nth-child(1) button")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")       # Círculo rojo con la cantidad
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")         # Ícono del carrito
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")            # Menú hamburguesa (☰)
    SORT_CONTAINER = (By.CLASS_NAME, "product_sort_container")  # Desplegable para ordenar

    def get_title(self):
        """Devuelve el título de la sección (debería ser 'Products')."""
        return self.get_text(self.TITLE_LABEL)

    def get_first_product_info(self):
        """Devuelve una tupla (nombre, precio) del primer producto del catálogo."""
        return self.get_text(self.FIRST_ITEM_NAME), self.get_text(self.FIRST_ITEM_PRICE)

    def add_first_product_to_cart(self):
        """
        Hace clic en 'Add to cart' del primer producto y espera a que aparezca
        el contador rojo del carrito, como confirmación de que se agregó.
        """
        self.click(self.FIRST_ADD_TO_CART_BTN)
        # Se espera la presencia del contador en el HTML: es más estable que
        # esperar a que sea visible en aplicaciones hechas con React
        self.wait.until(EC.presence_of_element_located(self.CART_BADGE))

    def get_cart_badge_count(self):
        """Devuelve el número que muestra el contador rojo del carrito (como texto)."""
        return self.get_text(self.CART_BADGE)

    def go_to_cart(self):
        """
        Hace clic en el ícono del carrito y espera a que la dirección (URL) cambie
        a 'cart.html', que confirma que se llegó a la pantalla del carrito.
        """
        self.click(self.CART_LINK)
        self.wait.until(EC.url_contains("cart.html"))

    def is_interface_loaded(self):
        """Devuelve True si se ven el menú y el selector de orden (la pantalla cargó bien)."""
        return self.is_displayed(self.MENU_BUTTON) and self.is_displayed(self.SORT_CONTAINER)

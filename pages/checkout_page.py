from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """
    Page Object correspondiente a las pantallas del flujo de pago (Checkout).
    """
    # Campos de datos personales del comprador
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_checkout_info(self, first_name, last_name, postal_code):
        """Completa el formulario de información del comprador y presiona Continuar."""
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)
        # Confirma la navegación al resumen de la orden por URL
        self.wait.until(EC.url_contains("checkout-step-two.html"))

    def finish_checkout(self):
        """
        Presiona el botón 'Finish' para confirmar la compra.
        Verifica la navegación a la pantalla de confirmación por URL.
        """
        self.click(self.FINISH_BUTTON)
        # Confirma la navegación a la pantalla de confirmación por URL
        self.wait.until(EC.url_contains("checkout-complete.html"))

    def get_completion_message(self):
        """Obtiene el texto del mensaje final de agradecimiento o confirmación de la orden."""
        return self.get_text(self.COMPLETE_HEADER)

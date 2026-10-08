import json
import os
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import setup_logger

logger = setup_logger()

def cargar_datos_usuarios():
    """Función auxiliar para leer e importar el archivo externo JSON de datos de prueba."""
    ruta_json = os.path.join(os.getcwd(), "datos", "usuarios.json")
    with open(ruta_json, "r", encoding="utf-8") as f:
        return json.load(f)

# Carga la fuente externa de datos al inicializar el módulo de pruebas
datos = cargar_datos_usuarios()


def test_01_login_exitoso(driver):
    """Caso de Prueba 1: Verificar el acceso exitoso al sistema usando un usuario válido."""
    logger.info("Ejecutando Test 01: Login Exitoso")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # Paso 1: Navegar a la página de login e ingresar credenciales válidas
    login_page.open()
    login_page.login(datos["usuario_valido"]["username"], datos["usuario_valido"]["password"])

    # Validación 1: Verificar que la URL actual cambió a la pantalla de inventario
    assert "/inventory.html" in driver.current_url
    # Validación 2: Confirmar que el título de la página principal sea 'Products'
    assert inventory_page.get_title() == "Products"


def test_02_login_fallido_escenario_negativo(driver):
    """Caso de Prueba 2 (Escenario Negativo): Validar que un usuario bloqueado reciba el error correspondiente."""
    logger.info("Ejecutando Test 02: Escenario Negativo Login")
    login_page = LoginPage(driver)

    # Paso 1: Intentar iniciar sesión con usuario bloqueado
    login_page.open()
    login_page.login(datos["usuario_bloqueado"]["username"], datos["usuario_bloqueado"]["password"])

    # Validación: Verificar que el mensaje de error desplegado sea el esperado
    mensaje_error = login_page.get_error_message()
    assert datos["usuario_bloqueado"]["mensaje_error"] in mensaje_error


def test_03_verificacion_catalogo_e_interfaz(driver):
    """Caso de Prueba 3: Validar la integridad de los elementos de la pantalla del catálogo."""
    logger.info("Ejecutando Test 03: Verificación de Catálogo")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # Iniciar sesión previa
    login_page.open()
    login_page.login(datos["usuario_valido"]["username"], datos["usuario_valido"]["password"])

    # Validación 1: Confirmar la visualización del menú y filtro de ordenamiento
    assert inventory_page.is_interface_loaded()
    
    # Validación 2: Verificar que el primer producto contenga nombre y precio válidos
    nombre, precio = inventory_page.get_first_product_info()
    assert nombre != "" and precio != ""


def test_04_agregar_producto_al_carrito(driver):
    """Caso de Prueba 4: Agregar un ítem al carrito y verificar su correcta adición."""
    logger.info("Ejecutando Test 04: Agregar al Carrito")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.open()
    login_page.login(datos["usuario_valido"]["username"], datos["usuario_valido"]["password"])

    # Captura el nombre del primer producto y lo agrega al carrito
    nombre_producto, _ = inventory_page.get_first_product_info()
    inventory_page.add_first_product_to_cart()

    # Validación 1: El contador rojo del carrito debe incrementarse a 1
    assert inventory_page.get_cart_badge_count() == "1"
    
    # Navega al carrito
    inventory_page.go_to_cart()

    # Validación 2: El producto presente en el carrito debe coincidir con el seleccionado
    assert cart_page.get_item_name() == nombre_producto


def test_05_flujo_completo_checkout(driver):
    """Caso de Prueba 5: Ejecución End-to-End de una compra completa hasta la confirmación."""
    logger.info("Ejecutando Test 05: Flujo Completo de Checkout")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # 1. Login
    login_page.open()
    login_page.login(datos["usuario_valido"]["username"], datos["usuario_valido"]["password"])

    # 2. Agregar ítem y avanzar al carrito
    inventory_page.add_first_product_to_cart()
    inventory_page.go_to_cart()

    # 3. Proceder al checkout y completar formulario con los datos cargados desde el JSON
    cart_page.proceed_to_checkout()
    checkout_page.fill_checkout_info(
        datos["datos_checkout"]["nombre"],
        datos["datos_checkout"]["apellido"],
        datos["datos_checkout"]["codigo_postal"]
    )
    
    # 4. Finalizar la orden
    checkout_page.finish_checkout()

    # Validación final: Mensaje de confirmación exitosa de la transacción
    assert checkout_page.get_completion_message() == "Thank you for your order!"
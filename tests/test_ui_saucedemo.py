"""
test_ui_saucedemo.py
--------------------
Pruebas automatizadas de interfaz (UI) sobre https://www.saucedemo.com

Cada test recibe el parámetro 'driver' (un Chrome nuevo, definido en conftest.py)
y usa los Page Objects de la carpeta 'pages/' para interactuar con el sitio.
Los datos de prueba (usuarios, contraseñas, datos del comprador) se leen del
archivo externo 'datos/usuarios.json'.

Casos:
  01 - Login exitoso (parametrizado: un test por cada usuario válido)
  02 - Login fallido / escenario negativo (parametrizado: un test por cada caso inválido)
  03 - Verificación del catálogo
  04 - Agregar un producto al carrito
  05 - Flujo completo de compra (End-to-End)
"""

import json
import os

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage
from utils.logger import setup_logger

logger = setup_logger()

# Ruta al archivo de datos. Se calcula a partir de la ubicación de este archivo,
# así funciona sin importar desde qué carpeta se ejecute pytest
RUTA_DATOS = os.path.join(os.path.dirname(__file__), "..", "datos", "usuarios.json")


def cargar_datos_usuarios():
    """Lee el archivo JSON de datos de prueba y lo devuelve como diccionario."""
    with open(RUTA_DATOS, "r", encoding="utf-8") as f:
        return json.load(f)


# Los datos se cargan una sola vez, al importar este archivo
datos = cargar_datos_usuarios()
# Usuario que se usa en los tests que necesitan estar logueados (03, 04 y 05)
usuario_checkout = datos["usuario_checkout"]


# @pytest.mark.parametrize ejecuta el mismo test una vez por cada elemento de la lista.
# 'ids' define el nombre que aparece entre corchetes en el reporte, ej: [standard_user]
@pytest.mark.parametrize(
    "usuario",
    datos["usuarios_validos"],
    ids=[u["username"] for u in datos["usuarios_validos"]],
)
def test_01_login_exitoso(driver, usuario):
    """Caso 1: con cada usuario válido del JSON, el login debe llevar al catálogo."""
    logger.info(f"Ejecutando Test 01: Login Exitoso con '{usuario['username']}'")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # Paso 1: abrir la página de login e ingresar las credenciales
    login_page.open()
    login_page.login(usuario["username"], usuario["password"])

    # Validación 1: la URL debe ser la del catálogo (inventory.html)
    assert "/inventory.html" in inventory_page.get_current_url()
    # Validación 2: el título de la pantalla debe ser 'Products'
    assert inventory_page.get_title() == "Products"


@pytest.mark.parametrize(
    "usuario",
    datos["usuarios_invalidos"],
    ids=[u["caso"] for u in datos["usuarios_invalidos"]],
)
def test_02_login_fallido_escenario_negativo(driver, usuario):
    """
    Caso 2 (escenario negativo): con cada combinación inválida del JSON
    (usuario bloqueado, contraseña incorrecta, campos vacíos) el sistema
    debe mostrar el mensaje de error correspondiente y no dejar ingresar.
    """
    logger.info(f"Ejecutando Test 02: Login fallido - caso '{usuario['caso']}'")
    login_page = LoginPage(driver)

    # Paso 1: intentar iniciar sesión con datos inválidos
    login_page.open()
    login_page.login(usuario["username"], usuario["password"])

    # Validación 1: el mensaje de error debe ser el esperado para este caso
    mensaje_error = login_page.get_error_message()
    assert usuario["mensaje_error"] in mensaje_error
    # Validación 2: no debe haber entrado al catálogo
    assert "/inventory.html" not in login_page.get_current_url()


def test_03_verificacion_catalogo_e_interfaz(driver):
    """Caso 3: después del login, el catálogo debe mostrar sus elementos principales."""
    logger.info("Ejecutando Test 03: Verificación de Catálogo")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # Paso previo: iniciar sesión
    login_page.open()
    login_page.login(usuario_checkout["username"], usuario_checkout["password"])

    # Validación 1: se ven el menú y el selector para ordenar productos
    assert inventory_page.is_interface_loaded()

    # Validación 2: el primer producto tiene nombre y un precio que empieza con '$'
    nombre, precio = inventory_page.get_first_product_info()
    assert nombre != ""
    assert precio.startswith("$")


def test_04_agregar_producto_al_carrito(driver):
    """Caso 4: agregar el primer producto al carrito y verificar que quedó agregado."""
    logger.info("Ejecutando Test 04: Agregar al Carrito")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    # Paso previo: iniciar sesión
    login_page.open()
    login_page.login(usuario_checkout["username"], usuario_checkout["password"])

    # Paso 1: guardar el nombre del primer producto y agregarlo al carrito
    nombre_producto, _ = inventory_page.get_first_product_info()
    inventory_page.add_first_product_to_cart()

    # Validación 1: el contador del carrito debe mostrar 1
    assert inventory_page.get_cart_badge_count() == "1"

    # Paso 2: ir al carrito
    inventory_page.go_to_cart()

    # Validación 2: el producto del carrito debe ser el mismo que se agregó
    assert cart_page.get_item_name() == nombre_producto


def test_05_flujo_completo_checkout(driver):
    """Caso 5 (End-to-End): compra completa, desde el login hasta la confirmación."""
    logger.info("Ejecutando Test 05: Flujo Completo de Checkout")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    # Las 3 pantallas del checkout, cada una con su propio Page Object
    information_page = CheckoutInformationPage(driver)
    overview_page = CheckoutOverviewPage(driver)
    complete_page = CheckoutCompletePage(driver)

    # 1. Iniciar sesión
    login_page.open()
    login_page.login(usuario_checkout["username"], usuario_checkout["password"])

    # 2. Guardar el nombre del primer producto, agregarlo e ir al carrito
    nombre_producto, _ = inventory_page.get_first_product_info()
    inventory_page.add_first_product_to_cart()
    inventory_page.go_to_cart()

    # 3. Pasar al checkout y completar el formulario con los datos del JSON
    cart_page.proceed_to_checkout()
    information_page.fill_information(
        datos["datos_checkout"]["nombre"],
        datos["datos_checkout"]["apellido"],
        datos["datos_checkout"]["codigo_postal"],
    )
    information_page.continue_to_overview()

    # Validación 1: el resumen de la orden muestra el producto elegido y un total en $
    assert overview_page.get_item_name() == nombre_producto
    assert "$" in overview_page.get_total()

    # 4. Confirmar la compra
    overview_page.finish()

    # Validación final: debe aparecer el mensaje de compra exitosa
    assert complete_page.get_completion_message() == "Thank you for your order!"

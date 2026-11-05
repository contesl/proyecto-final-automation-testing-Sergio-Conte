import requests
from utils.logger import setup_logger

logger = setup_logger()

# URL Base de la API pública de pruebas
BASE_URL = "https://reqres.in/api"

# Tiempo máximo de espera por respuesta (segundos)
TIMEOUT = 30


def log_respuesta(response):
    """Registra en el log el método, la URL y el código de estado de cada petición."""
    logger.info(
        f"{response.request.method} {response.url} -> {response.status_code} "
        f"({response.elapsed.total_seconds():.2f}s)"
    )


def test_api_get_users():
    """Caso de Prueba API 1 (GET): Consultar la lista de usuarios paginada."""
    logger.info("Ejecutando Test API GET /users?page=2")

    response = requests.get(f"{BASE_URL}/users", params={"page": 2}, timeout=TIMEOUT)
    log_respuesta(response)

    # Validación 1: Código de respuesta HTTP esperado (200 OK)
    assert response.status_code == 200

    # Validación 2: Estructura general del JSON y página solicitada
    json_data = response.json()
    assert json_data["page"] == 2
    assert "data" in json_data
    assert len(json_data["data"]) > 0  # Asegura que devuelva al menos un registro

    # Validación 3: Cada usuario debe tener los campos esperados
    campos_esperados = {"id", "email", "first_name", "last_name", "avatar"}
    for usuario in json_data["data"]:
        assert campos_esperados.issubset(usuario.keys())
        assert "@" in usuario["email"]


def test_api_create_user():
    """Caso de Prueba API 2 (POST): Registrar/Crear un nuevo usuario."""
    logger.info("Ejecutando Test API POST /users")

    # Cuerpo/Payload enviado en la petición en formato JSON
    payload = {"name": "Sergio Conte", "job": "QA Automation Engineer"}
    response = requests.post(f"{BASE_URL}/users", json=payload, timeout=TIMEOUT)
    log_respuesta(response)

    # Validación 1: Código de respuesta HTTP esperado para creación (201 Created)
    assert response.status_code == 201

    # Validación 2: Los datos devueltos en la respuesta deben coincidir con lo enviado
    json_data = response.json()
    assert json_data["name"] == payload["name"]
    assert json_data["job"] == payload["job"]
    assert "id" in json_data         # Debe haber generado un ID de recurso
    assert "createdAt" in json_data  # Debe informar la fecha de creación


def test_api_delete_user():
    """Caso de Prueba API 3 (DELETE): Eliminar un registro de usuario existente."""
    logger.info("Ejecutando Test API DELETE /users/2")

    response = requests.delete(f"{BASE_URL}/users/2", timeout=TIMEOUT)
    log_respuesta(response)

    # Validación: Código de respuesta HTTP esperado sin contenido (204 No Content)
    assert response.status_code == 204
    assert response.text == ""


def test_api_get_usuario_inexistente():
    """Caso de Prueba API 4 (Escenario de error - GET): consultar un usuario que no existe."""
    logger.info("Ejecutando Test API GET /users/23 (usuario inexistente)")

    response = requests.get(f"{BASE_URL}/users/23", timeout=TIMEOUT)
    log_respuesta(response)

    # Validación 1: La API debe responder 404 Not Found
    assert response.status_code == 404
    # Validación 2: El cuerpo debe ser un JSON vacío
    assert response.json() == {}


def test_api_login_sin_password():
    """Caso de Prueba API 5 (Escenario de error - POST): login sin enviar la contraseña."""
    logger.info("Ejecutando Test API POST /login sin password")

    payload = {"email": "peter@klaven"}
    response = requests.post(f"{BASE_URL}/login", json=payload, timeout=TIMEOUT)
    log_respuesta(response)

    # Validación 1: La API debe rechazar la petición con 400 Bad Request
    assert response.status_code == 400
    # Validación 2: El JSON de error debe indicar el motivo
    assert response.json() == {"error": "Missing password"}

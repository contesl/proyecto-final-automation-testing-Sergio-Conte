import requests
import pytest
from utils.logger import setup_logger

logger = setup_logger()
# URL Base de la API pública de pruebas
BASE_URL = "https://reqres.in/api"


def test_api_get_users():
    """Caso de Prueba API 1 (GET): Consultar la lista de usuarios paginada."""
    logger.info("Ejecutando Test API GET /users")
    
    # Envía solicitud HTTP GET
    response = requests.get(f"{BASE_URL}/users?page=2")

    # Validación 1: Código de respuesta HTTP esperado (200 OK)
    assert response.status_code == 200
    
    # Validación 2: Validar la estructura del cuerpo JSON retornado
    json_data = response.json()
    assert "data" in json_data
    assert len(json_data["data"]) > 0  # Asegura que devuelva al menos un registro


def test_api_create_user():
    """Caso de Prueba API 2 (POST): Registrar/Crear un nuevo usuario."""
    logger.info("Ejecutando Test API POST /users")
    
    # Cuerpo/Payload enviado en la petición en formato JSON
    payload = {"name": "Sergio Conte", "job": "QA Automation Engineer"}
    response = requests.post(f"{BASE_URL}/users", json=payload)

    # Validación 1: Código de respuesta HTTP esperado para creación (201 Created)
    assert response.status_code == 201
    
    # Validación 2: Los datos devueltos en la respuesta deben coincidir con lo enviado
    json_data = response.json()
    assert json_data["name"] == "Sergio Conte"
    assert json_data["job"] == "QA Automation Engineer"
    assert "id" in json_data  # Debe haber generado un ID de recurso


def test_api_delete_user():
    """Caso de Prueba API 3 (DELETE): Eliminar un registro de usuario existente."""
    logger.info("Ejecutando Test API DELETE /users/2")
    
    # Envía solicitud HTTP DELETE para el recurso id=2
    response = requests.delete(f"{BASE_URL}/users/2")

    # Validación: Código de respuesta HTTP esperado sin contenido (204 No Content)
    assert response.status_code == 204
"""
test_api_reqres.py
------------------
Pruebas automatizadas de API sobre ReqRes (https://reqres.in), una API pública
de práctica que simula un sistema de usuarios.

Estas pruebas no abren el navegador: envían peticiones HTTP con la biblioteca
'requests' y validan la respuesta (código de estado y contenido JSON).

Casos:
  1 - GET    /users?page=2  -> listar usuarios (éxito, 200)
  2 - POST   /users         -> crear un usuario (éxito, 201)
  3 - DELETE /users/2       -> eliminar un usuario (éxito, 204)
  4 - GET    /users/23      -> usuario inexistente (error, 404)
  5 - POST   /login         -> login sin contraseña (error, 400)
  6 - GET    /users  +  GET /users/{id}  -> peticiones encadenadas: se lista,
      se toma el id del primer usuario y se lo consulta individualmente
"""

import requests
from utils.logger import setup_logger

logger = setup_logger()

# Dirección base de la API: cada test le agrega el endpoint (ej: /users)
BASE_URL = "https://reqres.in/api"

# Tiempo máximo (en segundos) que se espera la respuesta antes de dar el test por fallido
TIMEOUT = 30


def log_respuesta(response):
    """Registra en el log el método, la URL, el código de estado y el tiempo de respuesta."""
    logger.info(
        f"{response.request.method} {response.url} -> {response.status_code} "
        f"({response.elapsed.total_seconds():.2f}s)"
    )


def test_api_get_users():
    """Caso API 1 (GET): obtener la página 2 de la lista de usuarios."""
    logger.info("Ejecutando Test API GET /users?page=2")

    # 'params' agrega ?page=2 al final de la URL
    response = requests.get(f"{BASE_URL}/users", params={"page": 2}, timeout=TIMEOUT)
    log_respuesta(response)

    # Validación 1: código 200 (OK)
    assert response.status_code == 200

    # Validación 2: la respuesta corresponde a la página pedida y trae usuarios
    json_data = response.json()
    assert json_data["page"] == 2
    assert "data" in json_data
    assert len(json_data["data"]) > 0

    # Validación 3: cada usuario tiene todos los campos esperados y un email válido
    campos_esperados = {"id", "email", "first_name", "last_name", "avatar"}
    for usuario in json_data["data"]:
        assert campos_esperados.issubset(usuario.keys())
        assert "@" in usuario["email"]


def test_api_create_user():
    """Caso API 2 (POST): crear un usuario nuevo."""
    logger.info("Ejecutando Test API POST /users")

    # Datos que se envían en el cuerpo de la petición, en formato JSON
    payload = {"name": "Sergio Conte", "job": "QA Automation Engineer"}
    response = requests.post(f"{BASE_URL}/users", json=payload, timeout=TIMEOUT)
    log_respuesta(response)

    # Validación 1: código 201 (Created = recurso creado)
    assert response.status_code == 201

    # Validación 2: la API devuelve los mismos datos enviados, más un id y la fecha de creación
    json_data = response.json()
    assert json_data["name"] == payload["name"]
    assert json_data["job"] == payload["job"]
    assert "id" in json_data
    assert "createdAt" in json_data


def test_api_delete_user():
    """Caso API 3 (DELETE): eliminar el usuario con id 2."""
    logger.info("Ejecutando Test API DELETE /users/2")

    response = requests.delete(f"{BASE_URL}/users/2", timeout=TIMEOUT)
    log_respuesta(response)

    # Validación: código 204 (No Content = eliminado, sin cuerpo en la respuesta)
    assert response.status_code == 204
    assert response.text == ""


def test_api_get_usuario_inexistente():
    """Caso API 4 (escenario de error - GET): pedir un usuario que no existe."""
    logger.info("Ejecutando Test API GET /users/23 (usuario inexistente)")

    response = requests.get(f"{BASE_URL}/users/23", timeout=TIMEOUT)
    log_respuesta(response)

    # Validación 1: código 404 (Not Found = no encontrado)
    assert response.status_code == 404
    # Validación 2: el cuerpo de la respuesta es un JSON vacío
    assert response.json() == {}


def test_api_login_sin_password():
    """Caso API 5 (escenario de error - POST): intentar loguearse sin enviar la contraseña."""
    logger.info("Ejecutando Test API POST /login sin password")

    # Se envía solo el email, a propósito sin el campo 'password'
    payload = {"email": "peter@klaven"}
    response = requests.post(f"{BASE_URL}/login", json=payload, timeout=TIMEOUT)
    log_respuesta(response)

    # Validación 1: código 400 (Bad Request = petición incorrecta)
    assert response.status_code == 400
    # Validación 2: el mensaje de error indica qué falta
    assert response.json() == {"error": "Missing password"}


def test_api_flujo_encadenado_listar_y_consultar_usuario():
    """
    Caso API 6 (peticiones encadenadas): la segunda petición depende del
    resultado de la primera.
      1. Se pide la lista de usuarios (GET /users?page=2).
      2. Se toma el id del primer usuario de esa lista.
      3. Se consulta ese usuario individualmente (GET /users/{id}).
      4. Se verifica que los datos coincidan en ambas respuestas.
    """
    logger.info("Ejecutando Test API encadenado: GET /users -> GET /users/{id}")

    # Petición 1: obtener la lista de usuarios
    respuesta_lista = requests.get(f"{BASE_URL}/users", params={"page": 2}, timeout=TIMEOUT)
    log_respuesta(respuesta_lista)
    assert respuesta_lista.status_code == 200

    # Se toma el primer usuario de la lista: su id se usa en la siguiente petición
    primer_usuario = respuesta_lista.json()["data"][0]
    id_usuario = primer_usuario["id"]
    logger.info(f"Id obtenido de la primera respuesta: {id_usuario}")

    # Petición 2: consultar ese usuario por su id
    respuesta_detalle = requests.get(f"{BASE_URL}/users/{id_usuario}", timeout=TIMEOUT)
    log_respuesta(respuesta_detalle)
    assert respuesta_detalle.status_code == 200

    # Validación: el usuario consultado es el mismo que figuraba en la lista
    usuario_detalle = respuesta_detalle.json()["data"]
    assert usuario_detalle["id"] == id_usuario
    assert usuario_detalle["email"] == primer_usuario["email"]
    assert usuario_detalle["first_name"] == primer_usuario["first_name"]
    assert usuario_detalle["last_name"] == primer_usuario["last_name"]

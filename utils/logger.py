"""
logger.py
---------
Configuración del sistema de logging (registro de eventos) del proyecto.

Cada mensaje que se registra con el logger se guarda en el archivo
reports/execution.log y además se muestra en la terminal. Sirve para seguir
paso a paso qué hizo cada test y encontrar rápido dónde falló.
"""

import logging
import os


def setup_logger(name="automation_logger"):
    """
    Crea (o reutiliza, si ya existe) el logger del proyecto y lo devuelve.

    Se puede llamar desde varios archivos: siempre devuelve el mismo logger,
    configurado una sola vez.
    """
    # Carpeta donde se guarda el log: 'reports/' dentro del proyecto
    log_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(log_dir, exist_ok=True)  # La crea si no existe

    # Ruta completa del archivo de log
    log_file = os.path.join(log_dir, "execution.log")

    # Obtiene el logger por su nombre (si ya fue creado, devuelve el mismo)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Registra mensajes de nivel INFO, WARNING y ERROR

    # Si el logger ya tiene "handlers" (destinos), ya fue configurado: no se repite,
    # porque si no cada mensaje aparecería duplicado
    if not logger.handlers:
        # Formato de cada línea: Fecha y hora - [Nivel] - Mensaje
        formato = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")

        # Destino 1: el archivo execution.log.
        # mode="w" hace que cada ejecución empiece con el archivo limpio,
        # así no se mezclan mensajes de corridas anteriores
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setFormatter(formato)
        logger.addHandler(file_handler)

        # Destino 2: la terminal (consola)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formato)
        logger.addHandler(console_handler)

    return logger

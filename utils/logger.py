import logging
import os

def setup_logger(name="automation_logger"):
    """
    Configura y retorna una instancia personalizada del Logger.
    Permite registrar eventos tanto en un archivo .log local como en la consola.
    """
    # Define la carpeta de destino del archivo de log ('reports/')
    log_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(log_dir, exist_ok=True)
    
    # Ruta completa donde se creará el archivo 'execution.log'
    log_file = os.path.join(log_dir, "execution.log")

    # Crea o recupera el logger con el nombre especificado
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Captura eventos desde nivel INFO en adelante

    # Evita agregar múltiples manejadores (handlers) si el logger ya fue configurado previamente
    if not logger.handlers:
        # 1. Handler para guardar los logs en un archivo físico
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        # Define el formato del log: Fecha/Hora - [Nivel] - Mensaje
        file_formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # 2. Handler para mostrar los logs en tiempo real por la consola (terminal)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_formatter)
        logger.addHandler(console_handler)

    return logger
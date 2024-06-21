import psycopg2
import os
from dotenv import load_dotenv

def is_postgres_service_active() -> bool:
    """
    Verifica si el servicio de PostgreSQL está activo en el sistema operativo.

    Returns:
        bool: True si el servicio está activo, False si no lo está
    """    
    
    load_dotenv()  # Cargar variables de entorno desde el archivo .env

    try:
        # Intentar conectar con la base de datos PostgreSQL utilizando las variables de entorno
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),  # Host de la base de datos
            port=os.getenv("DB_PORT"),  # Puerto de la base de datos
            dbname=os.getenv("DB_NAME"),  # Nombre de la base de datos
            user=os.getenv("DB_USER"),  # Usuario de la base de datos
            password=os.getenv("DB_PASSWORD")  # Contraseña del usuario de la base de datos
        )
        conn.close()  # Cerrar la conexión exitosa
        return True  # Devolver True si la conexión fue exitosa, lo que indica que el servicio está activo

    except psycopg2.OperationalError as e:
        # Si hay un error al conectar a la base de datos, se asume que el servicio no está activo
        return False  # Devolver False si ocurre un psycopg2.OperationalError, indicando que el servicio no está activo
    
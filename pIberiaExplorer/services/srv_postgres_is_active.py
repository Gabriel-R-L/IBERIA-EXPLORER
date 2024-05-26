import psycopg2
import os
from dotenv import load_dotenv

def is_postgres_service_active() -> bool:
    """
    Verificar si el servicio de postgresql esta activo en el sistema operativo

    Params: None

    ============================
    Returns: bool
    """
    load_dotenv()
    
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        # If there's an error connecting to the database, the service is likely inactive
        return False

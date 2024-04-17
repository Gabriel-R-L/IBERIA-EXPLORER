import os
import psycopg2
from django.apps import apps


def check_database() -> bool:
    """
    Comprobar si la base de datos existe y sus tablas

    Params: None

    ============================
    Returns: bool
    """

    # Buscar las variables de entorno para la conexión a la base de datos
    try:
        db_host = os.environ.get("DB_HOST")
        db_port = os.environ.get("DB_PORT")
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_password = os.environ.get("DB_PASSWORD")
    except Exception as e:
        print(f"Error al buscar las variables de entorno: {e}")
        return

    # Conectar a la base de datos
    conn = psycopg2.connect(
        host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
    )
    cursor = conn.cursor()

    # Comprobar si la base de datos
    cursor.execute(
        f"SELECT EXISTS(SELECT datname FROM pg_catalog.pg_database WHERE datname = {db_name});"
    )
    database_exists = cursor.fetchone()[0]

    conn.close()
    return True if database_exists else False

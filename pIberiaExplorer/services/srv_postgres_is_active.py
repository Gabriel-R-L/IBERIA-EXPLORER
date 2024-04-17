import psycopg2


def is_postgres_service_active() -> bool:
    """
    Verificar si el servicio de postgresql esta activo en el sistema operativo

    Params: None

    ============================
    Returns: bool
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="iberiaexplorerdb",
            user="postgres",
            password="Adivinala1."
        )
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        # If there's an error connecting to the database, the service is likely inactive
        return False

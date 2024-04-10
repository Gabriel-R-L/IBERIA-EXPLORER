import requests
import json
import os

# Rutas de los proyectos
path_proyecto = os.path.dirname(os.path.abspath(__file__))
path_proyecto_padre = os.path.dirname(path_proyecto)


def obtener_datos_desde_api():
    '''
        Función para obtener datos desde una API de ejemplo.
        
        Params: None
        
        ============================
        Returns: None
    '''
    
    
    # URL de la API de ejemplo
    url = (
        "https://datos.madrid.es/egob/catalogo/300107-0-agenda-actividades-eventos.json"
    )

    try:
        # Realizar la solicitud GET a la API
        response = requests.get(url)
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            datos = response.json()
            return datos
        else:
            # Imprimir mensaje de error si la solicitud no fue exitosa
            print(f"Error al obtener datos: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Capturar excepciones de solicitudes HTTP
        print(f"Error de conexión: {e}")
        return None


# Llamar a la función para obtener los datos desde la API
datos = obtener_datos_desde_api()


# Si los datos fueron obtenidos exitosamente, imprimirlos
if datos:
    # Guardar datos a un archivo json en la ruta del proyecto
    ruta_archivo = os.path.join(path_proyecto, f"{os.path.basename(__file__).split(".")[0]}.json")
    with open(ruta_archivo, "w") as archivo:
        json.dump(datos, archivo, indent=4)

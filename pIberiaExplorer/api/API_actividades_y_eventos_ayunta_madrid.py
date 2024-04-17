import requests
import os

import json

# Rutas de los proyectos
path_proyecto = os.path.dirname(os.path.abspath(__file__))
path_proyecto_padre = os.path.dirname(path_proyecto)


def obtener_datos_desde_api():
    """
    Función para obtener datos desde una API

    Params: None

    ============================
    Returns: None
    """

    # URL de la API de ejemplo
    url = (
        "https://datos.madrid.es/egob/catalogo/300107-0-agenda-actividades-eventos.json"
    )

    try:
        # Realizar la solicitud GET a la API
        response = requests.get(url)
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            datos = response.json()["@graph"]
            
            datos_finales = [crear_obj_formateado(dato) for dato in datos]
            
            # Guardar en archivo json
            with open(f"{path_proyecto_padre}/api/datos_actividades_eventos_madrid.json", "w", encoding="utf-8") as archivo:
                archivo.write(json.dumps(datos_finales, ensure_ascii=False))
            
            return datos_finales
        else:
            # Imprimir mensaje de error si la solicitud no fue exitosa
            print(f"Error al obtener datos: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Capturar excepciones de solicitudes HTTP
        print(f"Error de conexión: {e}")
        return None

def crear_obj_formateado(datos):
    """
    Función para crear un objeto formateado con los datos obtenidos desde la API

    Params:
    - datos: dict

    ============================
    Returns: dict
    """
    datos_tratados = {}
    for clave, valor in datos.items():
        # Reemplazar caracteres en las claves
        clave_formateada= clave.replace("@", "").replace("-", "")
        
        if isinstance(valor, dict):
            datos_tratados[clave_formateada] = crear_obj_formateado(valor)
        else:
            datos_tratados[clave_formateada] = valor
    return datos_tratados
import requests
import os

# Rutas de los proyectos
path_proyecto = os.path.dirname(os.path.abspath(__file__))
path_proyecto_padre = os.path.dirname(path_proyecto)

import locale
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8") # Para que se muestren los meses en español
from datetime import datetime


def obtener_datos_api():
    """
    Función para obtener datos desde una API

    Params: None

    ============================
    Returns: lista de diccionarios
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
            datos_necesarios = []
            
            # Guardar en archivo json
            # with open(f"{path_proyecto_padre}/api/datos_actividades_eventos_madrid.json", "w", encoding="utf-8") as archivo:
            #     archivo.write(json.dumps(datos_finales, ensure_ascii=False))
            
            for dato in datos_finales:
                try: 
                    fecha_inicio_original = dato["dtstart"].split(" ")[0]
                    fecha_fin_original = dato["dtend"].split(" ")[0]
                    descripcion = dato["description"]
                    if len(descripcion) < 400:
                        descripcion = dato["description"]
                    else:
                        descripcion = dato["description"][:400] + "..." + "<a href='%s'> Leer más</a>" % dato["link"]
                    
                    # Problema: algunos objetos dan error en dato["address"] y no devuelve dichos objetos
                    datos_necesarios.append(
                        {
                            "titulo": dato["title"],
                            "precio": dato["price"],
                            "descripcion": descripcion,
                            "fecha_inicio": datetime.strptime(fecha_inicio_original, "%Y-%m-%d").strftime("%d de %B de %Y"),
                            "fecha_fin": datetime.strptime(fecha_fin_original, "%Y-%m-%d").strftime("%d de %B de %Y"),
                            "hora_inicio": dato["time"],
                            "nombre_lugar": dato["address"]["area"]["locality"],
                            "codigo_postal": dato["address"]["area"]["postalcode"],
                            "nombre_calle": dato["address"]["area"]["streetaddress"],
                            "organizador": dato["organization"]["organizationname"],
                            "enlace_detalles": dato["link"]
                        }
                    )
                except KeyError as e:
                    print(f"Error al obtener datos: {e}")
                    continue # Continuar con la siguiente iteración del bucle
            
            return datos_necesarios
        else:
            # Imprimir mensaje de error si la solicitud no fue exitosa
            print(f"Error al obtener datos: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Capturar excepciones de solicitudes HTTP
        print(f"Error de conexión: {e}")
        return None

#? Esta función no sería necesaria puesto que con el objeto "datos_finales" ya se obtienen los datos necesarios
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
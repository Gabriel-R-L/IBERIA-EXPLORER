import requests
import os

# Rutas de los proyectos
path_proyecto = os.path.dirname(os.path.abspath(__file__))
path_proyecto_padre = os.path.dirname(path_proyecto)

import locale
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8") # Para que se muestren los meses en español
from datetime import date, datetime


def obtener_datos_api(tipo_plan: str = None, fecha_inicio: date = None, fecha_fin: date = None):
    """
    Obtiene los planes propuestos por el Ayuntamiento de Madrid desde la API. Si se especifica un tipo de plan, se obtienen solo los planes de ese tipo (dedicado a la views para ver planes similares).

    Args:
        tipo_plan (str, optional): Si se indica, solo se guardarán los que sean como el que se indica. Por defecto es None.
        
        fecha_inicio (date, optional): Fecha de inicio para filtrar los planes. Por defecto es None.
        
        fecha_fin (date, optional): Fecha de fin para filtrar los planes. Por defecto es None.

    Returns:
        List: Datos tratados de la API
    """
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
                    
                    # print("Fecha i ", fecha_inicio, "Fecha f ", fecha_fin, "Tipo p ", tipo_plan)
                    
                    # Guardar solo los que coincidan con el tipo de plan indicado
                    if tipo_plan is not None and tipo_plan  not in dato['type']:
                        continue
                    
                    # Guardar solo los que coincidan con la fecha de inicio y fin indicadas
                    if fecha_inicio is not None and datetime.strptime(fecha_inicio_original, "%Y-%m-%d") <= datetime.strptime(str(fecha_inicio), "%Y-%m-%d"):
                        continue
                    
                    if fecha_fin is not None and datetime.strptime(fecha_fin_original, "%Y-%m-%d") >= datetime.strptime(str(fecha_fin), "%Y-%m-%d"):
                        continue
                    
                    datos_necesarios.append(
                        {
                            "id_api": dato["id"],
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
                            "enlace_detalles": dato["link"],
                            "en_bd": False,
                            "url_tipo_plan": dato['type']
                        }
                    )
                    
                    # Ordenar los datos necesarios en base a la fecha de inicio
                    if fecha_inicio is not None:
                        datos_necesarios.sort(key=lambda x: datetime.strptime(x["fecha_inicio"], "%d de %B de %Y"))
                        
                    # Ordenar los datos necesarios en base a la fecha de fin
                    if fecha_fin and fecha_inicio is None:
                        datos_necesarios.sort(key=lambda x: datetime.strptime(x["fecha_fin"], "%d de %B de %Y"))
                except KeyError as e:
                    # print(f"Error al obtener datos: {e}")
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
    
    
def crear_obj_formateado(datos):
    """
    Función para crear un objeto formateado con los datos obtenidos desde la API

    Args:
        datos (dict): Datos obtenidos desde la API

    Returns:
        Dict: Datos formateados (sin caracteres raros, etc)
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
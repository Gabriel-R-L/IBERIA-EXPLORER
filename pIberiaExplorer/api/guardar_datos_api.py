import os
import sys
import re
import django

import locale
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8") # Para que se muestren los meses en español
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to the Python path
if project_root not in sys.path:
    sys.path.append(project_root)

# Set the environment variable for the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pIberiaExplorer.settings')
django.setup()

# Rutas de los proyectos
path_proyecto = os.path.dirname(os.path.abspath(__file__))
path_proyecto_padre = os.path.dirname(path_proyecto)

import locale
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8") # Para que se muestren los meses en español
from datetime import datetime

from Plantilla_API_Com_Madrid import obtener_datos_api
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
from appIberiaExplorer.models import Plan

def guardar_datos_api():
    """ 
        Método encargado de guardar los datos obtenidos de la API con un coste > 0
        en la base de datos
        
        Cuando el servidor activo, este archivo se ejecutará cada hora
        
        Params: None
        
        Returns: None
    """
    datos = obtener_datos_api()
    
    if datos is not None:
        for dato in datos:
            precio_str = dato['precio'].lower()
            titulo_str = dato['titulo'].lower()
            if 'euro' not in precio_str:
                continue
            
            price_match = re.search(r'(\d+(\.\d+)?)', precio_str)
            fecha_inicio = dato['fecha_inicio']
            fecha_fin = dato['fecha_fin']
            if price_match:
                precio = float(price_match.group(1))
            else:
                precio = 0
            if fecha_inicio:
                fecha_inicio = datetime.strptime(fecha_inicio, "%d de %B de %Y").strftime("%Y-%m-%d")
            else:
                fecha_inicio = None
            if fecha_fin:
                fecha_fin = datetime.strptime(fecha_fin, "%d de %B de %Y").strftime("%Y-%m-%d")
            else:
                fecha_fin = None
            if dato["descripcion"]:
                descripcion = dato["descripcion"]
                if len(descripcion) < 255:
                    descripcion = dato["descripcion"]
                else:
                    descripcion = dato["descripcion"][:200] + "..."
            else:
                descripcion = ""
            if dato['hora_inicio']:
                hora_inicio = dato['hora_inicio'] + ":00.000000"
            else:
                hora_inicio = None
            if dato["nombre_calle"]:
                nombre_calle = dato["nombre_calle"]
            else:
                nombre_calle = ""
                
            
            # El plan existe en la DB
            if not Plan.objects.filter(titulo=titulo_str).exists():
                plan = Plan.objects.create(
                    titulo=titulo_str,
                    descripcion=descripcion,
                    precio=precio,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    hora_inicio=hora_inicio,
                    nombre_lugar=nombre_calle
                )
                
                print(f"Plan {plan.titulo} creado")
    else: 
        print("No se han podido obtener los datos de la API")

if __name__ == '__main__':
    guardar_datos_api()

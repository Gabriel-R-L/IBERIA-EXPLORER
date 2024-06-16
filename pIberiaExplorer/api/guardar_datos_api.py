import os
import sys
import re
import django

import locale

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to the Python path
if project_root not in sys.path:
    sys.path.append(project_root)
    
# Set the environment variable for the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pIberiaExplorer.settings')
django.setup()


from appAjustes.models import UsuarioPreferencia
from appNotificaciones.models import Notificacion
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8") # Para que se muestren los meses en español
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

import locale
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8") # Para que se muestren los meses en español
from datetime import datetime

from api.Datos_API_Com_Madrid import obtener_datos_api
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
from appIberiaExplorer.models import Plan, AtributoPlan


def guardar_datos_api():
    """ 
        Método encargado de guardar los datos obtenidos de la API con un coste > 0
        en la base de datos
        
        Cuando el servidor activo, este archivo se ejecutará cada hora
        
        Params: None
        
        Returns: None
    """
    datos = obtener_datos_api()
    numero_planes_recomendados = 0
    
    if datos is not None:
        for dato in datos:
            id_plan_api = dato["id_api"]
            precio_str = dato['precio'].lower()
            price_match = re.search(r'(\d+(\.\d+)?)', precio_str)
            if 'euro' not in precio_str:
                continue
            titulo_str = dato['titulo'].lower()
            fecha_inicio_str = dato['fecha_inicio']
            fecha_fin_str = dato['fecha_fin']
            descripcion_str = dato['descripcion']
            nombre_calle_str = dato['nombre_calle']
            hora_inicio_str = dato['hora_inicio']
            url_tipo_plan = dato['url_tipo_plan']
            codigo_postal = dato['codigo_postal']
            organizador = dato['organizador']
            nombre_lugar = dato['nombre_lugar']
            
            
            if buscar_precio(precio_str):
                if not Plan.objects.filter(titulo=titulo_str).exists():
                    precio = float(price_match.group(1))
                    
                    if fecha_inicio_str:
                        fecha_inicio = datetime.strptime(fecha_inicio_str, "%d de %B de %Y").strftime("%Y-%m-%d")
                    else:
                        fecha_inicio = None
                        
                    if fecha_fin_str:
                        fecha_fin = datetime.strptime(fecha_fin_str, "%d de %B de %Y").strftime("%Y-%m-%d")
                    else:
                        fecha_fin = None
                        
                    if descripcion_str:
                        descripcion = descripcion_str
                        if len(descripcion) < 255:
                            descripcion = descripcion_str
                        else:
                            descripcion = descripcion_str[:200] + "..."
                    else:
                        descripcion = ""
                        
                    if hora_inicio_str:
                        hora_inicio = hora_inicio_str + ":00.000000"
                    else:
                        hora_inicio = None
                        
                    if nombre_calle_str:
                        nombre_calle = nombre_calle_str
                    else:
                        nombre_calle = ""
                    
                    plan = Plan.objects.create(
                        id_plan_api=id_plan_api,
                        titulo=titulo_str,
                        precio=precio,
                        descripcion=descripcion,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        hora_inicio=hora_inicio,
                        nombre_lugar=nombre_lugar,
                        codigo_postal=codigo_postal,
                        nombre_calle=nombre_calle,
                        organizador=organizador
                    )
                    print(f"Plan {plan.titulo} creado")
                    
                    if not AtributoPlan.objects.filter(plan=plan, nombre=url_tipo_plan).exists():
                        atributo_plan = AtributoPlan.objects.create(
                            plan=plan,
                            url=url_tipo_plan
                        )
                        
                        usuarios_preferencia = UsuarioPreferencia.objects.filter(atributo_plan=atributo_plan)
                        if usuarios_preferencia.exists() and numero_planes_recomendados < 5:
                            for usuario_preferencia in usuarios_preferencia:
                                Notificacion.objects.create(
                                    usuario=usuario_preferencia.usuario,
                                    titulo_notificacion=f"Se ha añadido un nuevo plan que puede ser de tu interés: {plan.titulo}",
                                    mensaje_notificacion=f"El plan con el atributo {atributo_plan.nombre} ha sido añadido. ¡No te lo pierdas!",
                                )
                                numero_planes_recomendados += 1
                                print(f"Plan {plan.titulo} añadido a la lista de planes recomendados para el usuario {usuario_preferencia.usuario.username}")
                                if numero_planes_recomendados >= 5:
                                    break
                        print(f"Atributo {atributo_plan.nombre} creado")
                    else:
                        print(f"Atributo {atributo_plan.nombre} ya existe")
                else:
                    print(f"Plan {titulo_str} ya existe")
            else:
                print(f"Plan {titulo_str} no cumple con las normas")
    else: 
        print("No se han podido obtener los datos de la API")


def buscar_precio(precio_str):
    """Funcion que comprueba el precio y si cumple con las normas

    Args:
        precio_str (str): precio del plan

    Returns:
        Boolean: True si los datos cumplen con las normas, False en caso contrario
    """
    price_match = re.search(r'(\d+(\.\d+)?)', precio_str)
    
    if not price_match:
        return False
        
    return True


if __name__ == '__main__':
    guardar_datos_api()
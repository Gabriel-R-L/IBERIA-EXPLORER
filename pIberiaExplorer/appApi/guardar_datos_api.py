import os
import sys
import re
import django
from datetime import datetime
import locale

# Define la raíz del proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Añadir la raíz del proyecto al path de Python
if project_root not in sys.path:
    sys.path.append(project_root)

# Establece la variable de entorno para la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pIberiaExplorer.settings')
django.setup()

# Configura la localización para mostrar los meses en español
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

# Importa las funciones y modelos necesarios de las aplicaciones Django
from appApi.Datos_API_Com_Madrid import obtener_datos_api
from appIberiaExplorer.models import Plan, AtributoPlan
from appAjustes.models import UsuarioPreferencia
from appNotificaciones.models import Notificacion

def guardar_datos_api():
    """
    Método encargado de guardar los datos obtenidos de la API con un coste > 0
    en la base de datos.
    
    Cuando el servidor está activo, este archivo debe ejecutarse cada hora.
    """
    # Obtiene los datos de la API
    datos = obtener_datos_api()
    
    if datos is not None:
        for dato in datos:
            id_plan_api = dato["id_api"]
            precio_str = dato['precio'].lower()
            price_match = re.search(r'(\d+(\.\d+)?)', precio_str)
            
            # Continúa solo si el precio está en euros
            if 'euro' not in precio_str:
                continue
            
            # Asigna variables a los campos de los datos obtenidos
            titulo_str = dato['titulo']
            fecha_inicio_str = dato['fecha_inicio']
            fecha_fin_str = dato['fecha_fin']
            descripcion_str = dato['descripcion']
            nombre_calle_str = dato['nombre_calle']
            hora_inicio_str = dato['hora_inicio']
            url_tipo_plan = dato['url_tipo_plan']
            codigo_postal = dato['codigo_postal']
            organizador = dato['organizador']
            nombre_lugar = dato['nombre_lugar']
            
            # Verifica si el precio cumple con las normas
            if buscar_precio(precio_str):
                # Verifica si el plan ya existe en la base de datos
                if not Plan.objects.filter(titulo=titulo_str).exists():
                    # Extrae el valor numérico del precio
                    precio = float(price_match.group(1))
                    
                    # Formatea las fechas de inicio y fin
                    if fecha_inicio_str:
                        fecha_inicio = datetime.strptime(fecha_inicio_str, "%d de %B de %Y").strftime("%Y-%m-%d")
                    else:
                        fecha_inicio = None
                        
                    if fecha_fin_str:
                        fecha_fin = datetime.strptime(fecha_fin_str, "%d de %B de %Y").strftime("%Y-%m-%d")
                    else:
                        fecha_fin = None
                        
                    # Gestiona la descripción del plan
                    if descripcion_str:
                        descripcion = descripcion_str
                        if len(descripcion) >= 255:
                            descripcion = descripcion_str[:200] + "..."
                    else:
                        descripcion = ""
                        
                    # Formatea la hora de inicio
                    if hora_inicio_str:
                        hora_inicio = hora_inicio_str + ":00.000000"
                    else:
                        hora_inicio = None
                        
                    if nombre_calle_str:
                        nombre_calle = nombre_calle_str
                    else:
                        nombre_calle = ""
                    
                    # Crea el nuevo plan en la base de datos
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
                    
                    # Verifica si el atributo del plan ya existe
                    if not AtributoPlan.objects.filter(plan=plan, url=url_tipo_plan).exists():
                        # Crea el nuevo atributo del plan
                        atributo_plan = AtributoPlan.objects.create(
                            plan=plan,
                            url=url_tipo_plan
                        )
                        
                        # Busca usuarios con preferencias que coincidan con el atributo
                        usuarios_preferencia = UsuarioPreferencia.objects.filter(atributo_plan=atributo_plan)
                        if usuarios_preferencia.exists():
                            for usuario_preferencia in usuarios_preferencia:
                                # Crea una notificación para cada usuario interesado
                                Notificacion.objects.create(
                                    usuario=usuario_preferencia.usuario,
                                    titulo_notificacion=f"Se ha añadido un nuevo plan que puede ser de tu interés: {plan.titulo}",
                                    mensaje_notificacion=f"Un plan con el atributo {atributo_plan.nombre} ha sido añadido. ¡No te lo pierdas!",
                                )
                                print(f"Plan {plan.titulo} añadido a la lista de planes recomendados para el usuario {usuario_preferencia.usuario.username}")
                        print(f"Atributo {atributo_plan.nombre} creado")
                else:
                    # Si el plan ya existe, verifica si el atributo del plan ya existe
                    plan = Plan.objects.get(titulo=titulo_str)

                    if not AtributoPlan.objects.filter(plan=plan, url=url_tipo_plan).exists():
                        # Crea el nuevo atributo del plan si no existe
                        atributo_plan = AtributoPlan.objects.create(
                            plan=plan,
                            url=url_tipo_plan
                        )
                        
                        # Busca usuarios con preferencias que coincidan con el atributo
                        usuarios_preferencia = UsuarioPreferencia.objects.filter(atributo_plan__nombre__icontains=atributo_plan.nombre)

                        if usuarios_preferencia.exists():
                            for usuario_preferencia in usuarios_preferencia:
                                # Crea una notificación para cada usuario interesado
                                Notificacion.objects.create(
                                    usuario=usuario_preferencia.usuario,
                                    titulo_notificacion=f"Se ha añadido un nuevo plan que puede ser de tu interés: {plan.titulo}",
                                    mensaje_notificacion=f"Un plan con el atributo {atributo_plan.nombre} ha sido añadido. ¡No te lo pierdas!",
                                )
                                print(f"Plan {plan.titulo} añadido a la lista de planes recomendados para el usuario {usuario_preferencia.usuario.username}")
                        print(f"Atributo {atributo_plan.nombre} creado")
                    print(f"Plan {titulo_str} ya existe")
            else:
                print(f"Plan {titulo_str} no cumple con las normas")
    else:
        print("No se han podido obtener los datos de la API")


def buscar_precio(precio_str):
    """
    Función que comprueba si el precio cumple con las normas.

    Args:
        precio_str (str): precio del plan

    Returns:
        Boolean: True si los datos cumplen con las normas, False en caso contrario
    """
    price_match = re.search(r'(\d+(\.\d+)?)', precio_str)
    
    if not price_match:
        return False
        
    return True

# Ejecuta la función principal si este archivo se ejecuta como script
if __name__ == '__main__':
    guardar_datos_api()

from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import *
from .models import *

from appApi.Datos_API_Com_Madrid import obtener_datos_api
from pIberiaExplorer.utils import APP_IBERIA_EXPLORER


#####################################################
# (API) ACTIVIDADES Y EVENTOS AYUNTAMIENTO DE MADRID
#####################################################
def resultado_datos_api(request):
    context = {}  # Contexto para pasar datos a la plantilla

    if request.method == "POST":
        # Si el método es POST, se procesa el formulario enviado
        form = BuscadorPreferenciaFecha(request.POST)
        if form.is_valid():
            # Si el formulario es válido, se obtienen los datos del formulario
            atributo_plan_id = form.cleaned_data['atributo_plan']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            
            # Si se ha seleccionado un atributo del plan
            if atributo_plan_id != '' or atributo_plan_id is None:
                # Se obtiene el nombre del atributo del plan, eliminando posibles barras
                nombre_ap = AtributoPlan.objects.get(id_atributo_plan=atributo_plan_id).nombre.replace("/", "")
                nombre_atributo = nombre_ap
                context["nombre_atributo"] = nombre_ap  # Se añade al contexto para la plantilla
            else:
                nombre_atributo = None

            # Se obtienen los datos de la API según los criterios de búsqueda
            datos = obtener_datos_api(tipo_plan=nombre_atributo, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            
            # Se vuelve a crear el formulario con los datos enviados y el atributo seleccionado
            form = BuscadorPreferenciaFecha(request.POST, selected_atributo_plan=atributo_plan_id)
        
        datos_pagina = datos  # Datos obtenidos de la API para la página actual
    else:
        # Si el método es GET, se obtienen todos los datos de la API sin filtros
        datos = obtener_datos_api()
        form = BuscadorPreferenciaFecha()  # Formulario vacío

        # Se pagina los datos obtenidos de la API
        paginator = Paginator(datos, 10)
        num_pagina = request.GET.get("page", 1)
        datos_pagina = paginator.get_page(num_pagina)
        
        # Determina la página siguiente y anterior para la paginación
        if datos_pagina.has_next():
            siguiente = datos_pagina.next_page_number()
        else:
            siguiente = 1
            
        if datos_pagina.has_previous():
            anterior = datos_pagina.previous_page_number()
        else:
            anterior = paginator.num_pages
            
        # Se añade al contexto para la plantilla
        context["siguiente"] = siguiente
        context["anterior"] = anterior
            
    # Total de datos obtenidos
    datos_totales = len(datos)
    
    # Obtiene los IDs de los planes de la API mostrados en la página actual
    id_planes_api = [int(dato["id_api"]) for dato in datos_pagina]
    
    # Filtra los planes que ya están en la base de datos según los IDs obtenidos
    planes_en_db = Plan.objects.filter(id_plan_api__in=id_planes_api)
    ids_planes_en_bd = set(planes_en_db.values_list("id_plan_api", flat=True))
    
    # Marca cada dato si ya está en la base de datos
    for dato in datos_pagina:
        dato_id = int(dato["id_api"])
        dato["en_bd"] = dato_id in ids_planes_en_bd
        
    # Añade los datos al contexto para la plantilla
    context["form"] = form
    context["datos"] = datos_pagina
    context["datos_totales"] = datos_totales

    # Renderiza la plantilla con el contexto
    return render(request, f"{APP_IBERIA_EXPLORER}/actividades_&_eventos_ayto_madrid.html", context=context)


###########################################
# INDEX
###########################################
def index(request):
    return render(request, f"{APP_IBERIA_EXPLORER}/index.html")


###########################################
# ACERCA DE
###########################################
def acerca_de(request):
    return render(request, f"{APP_IBERIA_EXPLORER}/info_TFG.html")


###########################################
# CONTACTO
###########################################
def contacto(request):
    return render(request, f"{APP_IBERIA_EXPLORER}/contacto.html")


###########################################
# PRIVACIDAD
###########################################
def privacidad(request):
    return render(request, f"{APP_IBERIA_EXPLORER}/politica_de_privacidad.html")


###########################################
# COOKIES
###########################################
def cookies(request):
    return render(request, f"{APP_IBERIA_EXPLORER}/uso_de_cookies.html")


###########################################
# FAQ
###########################################
def faq(request):
    return render(request, f"{APP_IBERIA_EXPLORER}/faq.html")


###########################################
# SOBRE NOSOTROS
###########################################
def sobre_nosotros(request):
    return render(request, f"{APP_IBERIA_EXPLORER}/equipo.html")
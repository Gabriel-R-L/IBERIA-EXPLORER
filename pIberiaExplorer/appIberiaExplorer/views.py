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
    context = {}
    if request.method == "POST":
        form = BuscadorPreferenciaFecha(request.POST)
        if form.is_valid():
            atributo_plan_id = form.cleaned_data['atributo_plan']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            if atributo_plan_id != '' or atributo_plan_id is None:
                nombre_ap =  AtributoPlan.objects.get(id_atributo_plan=atributo_plan_id).nombre.replace("/", "")
                nombre_atributo = nombre_ap
                context["nombre_atributo"] = nombre_ap
            else:
                nombre_atributo = None
            datos = obtener_datos_api(tipo_plan=nombre_atributo, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            form = BuscadorPreferenciaFecha(request.POST, selected_atributo_plan=atributo_plan_id)
        datos_pagina = datos
    else:
        datos = obtener_datos_api()
        form = BuscadorPreferenciaFecha()
        
        
        paginator = Paginator(datos, 10)
        num_pagina = request.GET.get("page", 1)
        datos_pagina = paginator.get_page(num_pagina)
        
        if datos_pagina.has_next():
            siguiente = datos_pagina.next_page_number()
        else:
            siguiente = 1
            
        if datos_pagina.has_previous():
            anterior = datos_pagina.previous_page_number()
        else:
            anterior = paginator.num_pages
            
        context["siguiente"] = siguiente
        context["anterior"] = anterior
            
    datos_totales = len(datos)
    id_planes_api = [int(dato["id_api"]) for dato in datos_pagina]
    planes_en_db = Plan.objects.filter(id_plan_api__in=id_planes_api)
    ids_planes_en_bd = set(planes_en_db.values_list("id_plan_api", flat=True))
    
    for dato in datos_pagina:
        dato_id = int(dato["id_api"])
        dato["en_bd"] = dato_id in ids_planes_en_bd
        
    context["form"] = form
    context["datos"] = datos_pagina
    context["datos_totales"] = datos_totales
    

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
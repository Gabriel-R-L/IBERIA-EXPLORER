import select
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from django.conf import settings
from django.db import IntegrityError

from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.core.mail import send_mail

import os
import sys
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


from datetime import timezone
import urllib.request as urllib

from .forms import *
from .models import *

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from spanlp.palabrota import Palabrota
from django.utils.crypto import get_random_string

from api.Datos_API_Com_Madrid import obtener_datos_api

from django.core.paginator import Paginator

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt

from pIberiaExplorer.utils import APP_IBERIA_EXPLORER


###########################################
# (API) Actividades y eventos de Ayto. Madrid
###########################################
def resultado_datos_api(request):
    context = {}
    if request.method == "POST":
        form = MostrarPreferencia(request.POST)
        if form.is_valid():
            atributo_plan_id = request.POST['atributo_plan']
            nombre_atributo = AtributoPlan.objects.get(id_atributo_plan=atributo_plan_id).nombre.replace("/", "")
            datos = obtener_datos_api(nombre_atributo)
            form = MostrarPreferencia(request.POST, selected_atributo_plan=atributo_plan_id)
            
            context["nombre_atributo"] = AtributoPlan.objects.get(id_atributo_plan=atributo_plan_id).nombre
    else:
        datos = obtener_datos_api()
        form = MostrarPreferencia()
        
        
    datos_totales = len(datos)
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
        
    id_planes_api = [int(dato["id_api"]) for dato in datos_pagina]
    planes_en_db = Plan.objects.filter(id_plan_api__in=id_planes_api)
    ids_planes_en_bd = set(planes_en_db.values_list("id_plan_api", flat=True))
    
    for dato in datos_pagina:
        dato_id = int(dato["id_api"])
        dato["en_bd"] = dato_id in ids_planes_en_bd
        
    context["form"] = form
    context["datos"] = datos_pagina
    context["datos_totales"] = datos_totales
    context["siguiente"] = siguiente
    context["anterior"] = anterior

    return render(request, f"{APP_IBERIA_EXPLORER}/actividades_&_eventos_ayto_madrid.html", context=context)


###########################################
# Index
###########################################
def index(request):
    return render(request, f"{APP_IBERIA_EXPLORER}/index.html")

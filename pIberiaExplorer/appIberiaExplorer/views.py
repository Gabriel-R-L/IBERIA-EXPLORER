from django.shortcuts import redirect, render
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

from api.Plantilla_API_Com_Madrid import obtener_datos_api

from django.core.paginator import Paginator

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt


###########################################
# (API) Actividades y eventos de Ayto. Madrid
def resultado_datos_api(request):
    datos = obtener_datos_api()
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
    
    context = {
        "datos": datos_pagina,
        "datos_totales": datos_totales,
        "siguiente": siguiente,
        "anterior": anterior,
    }
    
    return render(request, "actividades_&_eventos_ayto_madrid.html", context=context)


###########################################
# Index
def index(request):
    return render(request, "index.html")


from django.urls import path, include
from .views import *

from pIberiaExplorer.utils import APP_IBERIA_EXPLORER
app_name = APP_IBERIA_EXPLORER

urlpatterns = [
    path("", index, name="index"),
    
    # Resultados de API
    path("actividades_&_eventos_ayto_madrid/", resultado_datos_api, name="resultado_datos_api",
    ),
    
    # Otros
    path("acerca_de/", acerca_de, name="acerca_de"), # info_TFG.html
    path("contacto/", contacto, name="contacto"), # contacto.html
    path("privacidad/", privacidad, name="privacidad"), # politica_de_privacidad.html
    path("cookies/", cookies, name="cookies"), # uso_de_cookies.html
    path("faq/", faq, name="faq"), # faq.html
    path("sobre_nosotros/", sobre_nosotros, name="sobre_nosotros"), # equipo.html
]

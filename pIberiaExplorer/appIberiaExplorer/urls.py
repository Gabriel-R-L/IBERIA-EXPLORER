from django.urls import path, include
from .views import *

app_name = "appIberiaExplorer"

urlpatterns = [
    path("", index, name="index"),
    
    # Resultados de API
    path(
        "actividades_&_eventos_ayto_madrid/",
        resultado_datos_api,
        name="resultado_datos_api",
    ),
]

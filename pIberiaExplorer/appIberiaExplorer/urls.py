from django.urls import path
from .views import *

app_name = "appIberiaExplorer"

urlpatterns = [
    path("", index, name="index"),
    # CRUD usuario
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    # Confirmar correo
    path("confirm_email/<str:token>/", confirm_email, name="confirm_email"),
    path("email_confirmed/", email_confirmed, name="email_confirmed"),
    # Resultados de API
    path(
        "actividades_&_eventos_ayto_madrid/",
        resultado_datos_api,
        name="resultado_datos_api",
    ),
]

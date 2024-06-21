from django.urls import path
from .views import *

from pIberiaExplorer.utils import APP_AJUSTES
app_name = APP_AJUSTES

urlpatterns = [
    path('configuracion-cuenta/', configuracion_cuenta, name='configuracion_cuenta'),
    path('mis-datos/', ver_datos, name='ver_datos'),
    path('agregar-preferencia/', añadir_preferencia, name='añadir_preferencia'),
    path('borrar-preferencia/<int:id_preferencia>/', borrar_preferencia, name='borrar_preferencia'),
]
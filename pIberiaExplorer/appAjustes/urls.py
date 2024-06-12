from django.urls import path
from .views import *

app_name = 'appAjustes'

urlpatterns = [
    path('configuracion-cuenta/', configuracion_cuenta, name='configuracion_cuenta'),
    path('mis-datos/', ver_datos, name='ver_datos'),
    path('agregar-preferencia/', añadir_preferencia, name='añadir_preferencia'),
    path('borrar-preferencia/<int:id_preferencia>/', borrar_preferencia, name='borrar_preferencia'),
    path('cambiar-foto-perfil/', cambiar_foto_perfil, name='cambiar_foto_perfil'),
]
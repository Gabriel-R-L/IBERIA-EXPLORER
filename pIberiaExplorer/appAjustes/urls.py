from django.urls import path
from .views import *

app_name = 'appAjustes'

urlpatterns = [
    path('configuracion-cuenta/', configuracion_cuenta, name='configuracion_cuenta'),
]
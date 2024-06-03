from django.urls import path
from .views import *

app_name = 'appNotificaciones'

urlpatterns = [
    path('', ver_notificaciones, name='ver_notificaciones'),
    path('notificacion/<int:id>/', ver_notificacion, name='ver_notificacion'),
    path('eliminar_notificacion/<int:id>/', eliminar_notificacion, name='eliminar_notificacion'),
    path('eliminar_notificaciones/', eliminar_notificaciones, name='eliminar_notificaciones'),
]

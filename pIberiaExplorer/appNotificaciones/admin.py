from django.contrib import admin
from .models import Notificacion
admin.site.site_header = "SITIO DE ADMINISTRACIÓN DE NOTIFICACIONES"
admin.site.site_title = "SITIO DE ADMINISTRACIÓN DE NOTIFICACIONES"
admin.site.index_title = "Bienvenido al portal de Administración"


############################################
# NOTIFICACIONES
############################################
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['id','usuario', 'titulo_notificacion', 'mensaje_notificacion', 'timestamp', 'leido']
    search_fields = ('id','usuario', 'titulo_notificacion', 'mensaje_notificacion', 'timestamp', 'leido')
    list_filter = ('id','usuario', 'titulo_notificacion', 'mensaje_notificacion', 'timestamp', 'leido')
admin.site.register(Notificacion, NotificacionAdmin)

from django.contrib import admin
from .models import Notificacion

class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['id','usuario', 'titulo_notificacion', 'mensaje_notificacion', 'timestamp', 'leido']
    search_fields = ('id','usuario', 'titulo_notificacion', 'mensaje_notificacion', 'timestamp', 'leido')
    list_filter = ('id','usuario', 'titulo_notificacion', 'mensaje_notificacion', 'timestamp', 'leido')
admin.site.register(Notificacion, NotificacionAdmin)

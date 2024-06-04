from django.contrib import admin
from .models import Usuario
admin.site.site_header = "SITIO DE ADMINISTRACIÓN DE USUARIOS"  #este es el título
admin.site.site_title = "SITIO DE ADMINISTRACIÓN DE USUARIOS" #este es el título
admin.site.index_title = "Bienvenido al portal de Administración" #este es el título

# 9 Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'username', 'apellido_1', 'email', 'telefono', 'fecha_baja']
    search_fields = ('id_usuario', 'username', 'apellido_1', 'email', 'telefono', 'fecha_baja')
    list_filter = ('id_usuario', 'username', 'apellido_1', 'email', 'telefono', 'fecha_baja')
admin.site.register(Usuario, UsuarioAdmin)
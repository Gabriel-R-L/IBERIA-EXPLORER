from django.contrib import admin
from .models import UsuarioPreferencia
admin.site.site_header = "SITIO DE ADMINISTRACIÓN DE AJUSTES"
admin.site.site_title = "SITIO DE ADMINISTRACIÓN DEL AJUSTES"
admin.site.index_title = "Bienvenido al portal de Administración"


####################################################
# USUARIOPREFERENCIA
####################################################
class UsuarioPreferenciaAdmin(admin.ModelAdmin):
    list_display = ['id_preferencia', 'usuario', 'atributo_plan']
    search_fields = ('id_preferencia', 'usuario', 'atributo_plan')
    list_filter = ('id_preferencia', 'usuario', 'atributo_plan')
admin.site.register(UsuarioPreferencia, UsuarioPreferenciaAdmin)
from django.contrib import admin
from .models import UsuarioPreferencia

####################################################
# UsuarioPreferencia
####################################################
class UsuarioPreferenciaAdmin(admin.ModelAdmin):
    list_display = ['id_preferencia', 'usuario', 'atributo_plan']
    search_fields = ('id_preferencia', 'usuario', 'atributo_plan')
    list_filter = ('id_preferencia', 'usuario', 'atributo_plan')
admin.site.register(UsuarioPreferencia, UsuarioPreferenciaAdmin)
from django.contrib import admin
from .models import *
admin.site.site_header = "SITIO DE ADMINISTRACIÓN DE IBERIA EXPLORER"
admin.site.site_title = "Portal de Administración de Iberia Explorer"
admin.site.index_title = "Bienvenido al portal de Administración"


####################################################
# CONTINENTE
####################################################
class ContinenteAdmin(admin.ModelAdmin):
    list_display = ['id_continente', 'nombre']
    search_fields = ('id_continente', 'nombre')
    list_filter = ('id_continente', 'nombre')   
admin.site.register(Continente, ContinenteAdmin)


####################################################
# PAIS
####################################################
class PaisAdmin(admin.ModelAdmin):
    list_display = ['id_pais', 'nombre', 'continente']
    search_fields = ('id_pais', 'nombre', 'continente')
    list_filter = ('id_pais', 'nombre', 'continente')
admin.site.register(Pais, PaisAdmin)


####################################################
# CIUDAD
####################################################
class CiudadAdmin(admin.ModelAdmin):
    list_display = ['id_ciudad', 'nombre', 'pais']
    search_fields = ('id_ciudad', 'nombre', 'pais')
    list_filter = ('id_ciudad', 'nombre', 'pais')
admin.site.register(Ciudad, CiudadAdmin)


####################################################
# PLAN
####################################################
class PlanAdmin(admin.ModelAdmin):
    list_display = ['id_plan', 'id_plan_api', 'titulo', 'precio', 'fecha_inicio', 'fecha_fin', 'hora_inicio', 'nombre_lugar', 'codigo_postal', 'nombre_calle', 'organizador']
    search_fields = ('id_plan', 'id_plan_api', 'titulo', 'precio', 'fecha_inicio', 'fecha_fin', 'hora_inicio', 'nombre_lugar', 'codigo_postal', 'nombre_calle', 'organizador')
    list_filter = ('id_plan', 'id_plan_api', 'titulo', 'precio', 'fecha_inicio', 'fecha_fin', 'hora_inicio', 'nombre_lugar', 'codigo_postal', 'nombre_calle', 'organizador')
admin.site.register(Plan, PlanAdmin)


####################################################
# ATRIBUTOPLAN
####################################################
class AtributoPlanAdmin(admin.ModelAdmin):
    list_display = ['id_atributo_plan', 'nombre', 'url', 'plan']
    search_fields = ('id_atributo_plan', 'nombre', 'url', 'plan')
    list_filter = ('id_atributo_plan', 'nombre', 'url', 'plan')
admin.site.register(AtributoPlan, AtributoPlanAdmin)


######################################################################################################################################
######################################################################################################################################

# 5 Proveedor
""" class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['id_proveedor', 'nombre', 'direccion', 'telefono', 'email', 'id_ciudad', 'id_pais']
    search_fields = ('id_proveedor', 'nombre', 'direccion', 'telefono', 'email', 'id_ciudad', 'id_pais')
    list_filter = ('id_proveedor', 'nombre', 'direccion', 'telefono', 'email', 'id_ciudad', 'id_pais')
admin.site.register(Proveedor, ProveedorAdmin) """

# 6 TipoPlan
""" class TipoPlanAdmin(admin.ModelAdmin):
    list_display = ['id_tipo_plan', 'nombre_tipo_plan']
    search_fields = ('id_tipo_plan', 'nombre_tipo_plan')
    list_filter = ('id_tipo_plan', 'nombre_tipo_plan')
admin.site.register(TipoPlan, TipoPlanAdmin )"""



# 10 Reserva
# class ReservaAdmin(admin.ModelAdmin):
#     list_display = ['id_reserva', 'fecha_reserva', 'id_plan']
#     search_fields = ('id_reserva', 'fecha_reserva', 'id_plan')
#     list_filter = ('id_reserva', 'fecha_reserva', 'id_plan')
# admin.site.register(Reserva, ReservaAdmin)

# 11 Comentario
""" class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['id_comentario', 'comentario', 'id_usuario', 'id_plan']
    search_fields = ('id_comentario', 'comentario', 'id_usuario', 'id_plan')
    list_filter = ('id_comentario', 'comentario', 'id_usuario', 'id_plan')
admin.site.register(Comentario, ComentarioAdmin) """

# 13 EstadoRerserva
# class EstadoReservaAdmin(admin.ModelAdmin):
#     list_display = ['id_estado_reserva', 'nombre']
#     search_fields = ('id_estado_reserva', 'nombre')
#     list_filter = ('id_estado_reserva', 'nombre')
# admin.site.register(EstadoReserva, EstadoReservaAdmin)

# 14 Reserva
# class FavoritoAdmin(admin.ModelAdmin):
#     list_display = ['id_favorito', 'id_usuario', 'id_plan']
#     search_fields = ('id_favorito', 'id_usuario', 'id_plan')
#     list_filter = ('id_favorito', 'id_usuario', 'id_plan')
# admin.site.register(Favorito, FavoritoAdmin)

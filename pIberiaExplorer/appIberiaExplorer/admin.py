# Register your models here.
# create admin
from django.contrib import admin
from .models import *
admin.site.site_header = "SITIO DE ADMINISTRACIÓN DE IBERIA EXPLORER"  #este es el título
admin.site.site_title = "SITIO DE ADMINISTRACIÓN DE IBERIA EXPLORER" #este es el título
admin.site.index_title = "Bienvenido al portal de Administración" #este es el título

# 1 Continente
class ContinenteAdmin(admin.ModelAdmin):
    list_display = ['id_continente', 'nombre']
    search_fields = ('id_continente', 'nombre')
    list_filter = ('id_continente', 'nombre')   
admin.site.register(Continente, ContinenteAdmin)

# 2 Pais
class PaisAdmin(admin.ModelAdmin):
    list_display = ['id_pais', 'nombre', 'id_continente']
    search_fields = ('id_pais', 'nombre', 'id_continente')
    list_filter = ('id_pais', 'nombre', 'id_continente')
admin.site.register(Pais, PaisAdmin)

# 3 Ciudad
class CiudadAdmin(admin.ModelAdmin):
    list_display = ['id_ciudad', 'nombre', 'id_pais', 'id_continente']
    search_fields = ('id_ciudad', 'nombre', 'id_pais', 'id_continente')
    list_filter = ('id_ciudad', 'nombre', 'id_pais', 'id_continente')
admin.site.register(Ciudad, CiudadAdmin)

# 4 AtributoPlan
class AtributoPlanAdmin(admin.ModelAdmin):
    list_display = ['id_atributo_plan', 'nombre']
    search_fields = ('id_atributo_plan', 'nombre')
    list_filter = ('id_atributo_plan', 'nombre')
admin.site.register(AtributoPlan, AtributoPlanAdmin)

# 5 Proveedor
""" class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['id_proveedor', 'nombre', 'direccion', 'telefono', 'email', 'id_ciudad', 'id_pais']
    search_fields = ('id_proveedor', 'nombre', 'direccion', 'telefono', 'email', 'id_ciudad', 'id_pais')
    list_filter = ('id_proveedor', 'nombre', 'direccion', 'telefono', 'email', 'id_ciudad', 'id_pais')
admin.site.register(Proveedor, ProveedorAdmin) """

# 6 TipoPlan
class TipoPlanAdmin(admin.ModelAdmin):
    list_display = ['id_tipo_plan', 'nombre_tipo_plan']
    search_fields = ('id_tipo_plan', 'nombre_tipo_plan')
    list_filter = ('id_tipo_plan', 'nombre_tipo_plan')
admin.site.register(TipoPlan, TipoPlanAdmin)

# 7 Plan
class PlanAdmin(admin.ModelAdmin):
    list_display = ['id_plan', 'titulo', 'precio', 'fecha_inicio', 'fecha_fin', 'hora_inicio', 'nombre_lugar', 'codigo_postal', 'nombre_calle', 'organizador']
    search_fields = ('id_plan', 'titulo', 'precio', 'fecha_inicio', 'fecha_fin', 'hora_inicio', 'nombre_lugar', 'codigo_postal', 'nombre_calle', 'organizador')
    list_filter = ('id_plan', 'titulo', 'precio', 'fecha_inicio', 'fecha_fin', 'hora_inicio', 'nombre_lugar', 'codigo_postal', 'nombre_calle', 'organizador')
admin.site.register(Plan, PlanAdmin)

# 8 UsuarioPreferencias
class UsuarioPreferenciaAdmin(admin.ModelAdmin):
    list_display = ['id_preferencia', 'id_usuario', 'id_atributo_plan_plan']
    search_fields = ('id_preferencia', 'id_usuario', 'id_atributo_plan_plan')
    list_filter = ('id_preferencia', 'id_usuario', 'id_atributo_plan_plan')
admin.site.register(UsuarioPreferencia, UsuarioPreferenciaAdmin)

# 10 Reserva
# class ReservaAdmin(admin.ModelAdmin):
#     list_display = ['id_reserva', 'fecha_reserva', 'id_plan']
#     search_fields = ('id_reserva', 'fecha_reserva', 'id_plan')
#     list_filter = ('id_reserva', 'fecha_reserva', 'id_plan')
# admin.site.register(Reserva, ReservaAdmin)

# 11 Comentario
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['id_comentario', 'comentario', 'id_usuario', 'id_plan']
    search_fields = ('id_comentario', 'comentario', 'id_usuario', 'id_plan')
    list_filter = ('id_comentario', 'comentario', 'id_usuario', 'id_plan')
admin.site.register(Comentario, ComentarioAdmin)

# 12 Notificacion
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['id_notificacion', 'texto_notificacion', 'id_usuario']
    search_fields = ('id_notificacion', 'texto_notificacion', 'id_usuario')
    list_filter = ('id_notificacion', 'texto_notificacion', 'id_usuario')
admin.site.register(Notificacion, NotificacionAdmin)

# 13 EstadoRerserva
class EstadoReservaAdmin(admin.ModelAdmin):
    list_display = ['id_estado_reserva', 'nombre']
    search_fields = ('id_estado_reserva', 'nombre')
    list_filter = ('id_estado_reserva', 'nombre')
admin.site.register(EstadoReserva, EstadoReservaAdmin)

# 14 Reserva
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['id_favorito', 'id_usuario', 'id_plan']
    search_fields = ('id_favorito', 'id_usuario', 'id_plan')
    list_filter = ('id_favorito', 'id_usuario', 'id_plan')
admin.site.register(Favorito, FavoritoAdmin)

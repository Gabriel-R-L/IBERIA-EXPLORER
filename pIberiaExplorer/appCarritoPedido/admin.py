from django.contrib import admin
from .models import Carrito, CarritoDetalle, Pedido, PedidoDetalle
admin.site.site_header = "SITIO DE ADMINISTRACIÓN DEL CARRITO Y PEDIDO"
admin.site.site_title = "SITIO DE ADMINISTRACIÓN DEL CARRITO Y PEDIDO"
admin.site.index_title = "Bienvenido al portal de Administración"


#####################################
# CARRITO
#####################################
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['id_carrito', 'id_usuario']
    search_fields = ('id_carrito', 'id_usuario')
    list_filter = ('id_carrito', 'id_usuario')
admin.site.register(Carrito, CarritoAdmin)

class CarritoDetalleAdmin(admin.ModelAdmin):
    list_display = ['id_carrito_detalle', 'id_carrito', 'id_plan', 'cantidad']
    search_fields = ('id_carrito_detalle', 'id_carrito', 'id_plan', 'cantidad')
    list_filter = ('id_carrito_detalle', 'id_carrito', 'id_plan', 'cantidad')
admin.site.register(CarritoDetalle, CarritoDetalleAdmin)


#####################################
# PEDIDO
#####################################
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id_pedido', 'id_cliente', 'total', 'fecha_reserva', 'estado']
    search_fields = ('id_pedido', 'id_cliente', 'total', 'fecha_reserva', 'estado')
    list_filter = ('id_pedido', 'id_cliente', 'total', 'fecha_reserva', 'estado')
admin.site.register(Pedido, PedidoAdmin)

class PedidoDetalleAdmin(admin.ModelAdmin):
    list_display = ['id_pedido_detalle', 'id_pedido', 'id_plan', 'cantidad']
    search_fields = ('id_pedido_detalle', 'id_pedido', 'id_plan', 'cantidad')
    list_filter = ('id_pedido_detalle', 'id_pedido', 'id_plan', 'cantidad')
admin.site.register(PedidoDetalle, PedidoDetalleAdmin)
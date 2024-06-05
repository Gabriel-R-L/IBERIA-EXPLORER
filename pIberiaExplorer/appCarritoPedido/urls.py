from django.urls import path, include
from .views import *

app_name = "appCarritoPedido"

urlpatterns = [
    # Carrito
    path("", ver_carrito, name="ver_carrito"),
    path("agregar/<int:id_plan>/", agregar_al_carrito, name="agregar_al_carrito"),
    path("actualizar/<int:detalle_id>/", actualizar_carrito, name="actualizar_carrito"),
    path("eliminar/<int:detalle_id>/", eliminar_del_carrito, name="eliminar_del_carrito"),
    
    # Pedidos
    path('pedido/completar/', completar_pedido, name='completar_pedido'),
    path('pedidos/', ver_pedidos, name='ver_pedidos'),
    path('pedido/<int:pedido_id>/', ver_pedido_detalle, name='ver_pedido_detalle'),
    path('pagar_pedidos/', pagar_pedidos, name='pagar_pedidos'),
    path('completar_pago/', completar_pago, name='completar_pago'),
    path('cancelar_pedido/<int:pedido_id>/', cancelar_pedido, name='cancelar_pedido'),
]

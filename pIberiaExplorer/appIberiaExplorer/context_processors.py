from appCarritoPedido.models import Carrito, CarritoDetalle

# Función para añadir el contexto del carrito de la compra
def carrito_context(request):
    if request.user.is_authenticated:
        # Si el usuario está autenticado, se obtiene el carrito de la compra
        carrito = Carrito.objects.filter(id_usuario=request.user).first()
        if carrito:
            # Si el carrito existe, se obtiene la cantidad total de productos
            detalles = CarritoDetalle.objects.filter(id_carrito=carrito)
            cantidad_total = sum(item.cantidad for item in detalles)
        else:
            cantidad_total = 0
    else:
        cantidad_total = 0

    return {
        'cantidad_total': cantidad_total
    }
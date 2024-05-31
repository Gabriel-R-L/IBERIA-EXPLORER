from appCarritoPedido.models import Carrito, CarritoDetalle

def carrito_context(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(id_usuario=request.user).first()
        if carrito:
            detalles = CarritoDetalle.objects.filter(id_carrito=carrito)
            cantidad_total = sum(item.cantidad for item in detalles)
        else:
            cantidad_total = 0
    else:
        cantidad_total = 0

    return {
        'cantidad_total': cantidad_total
    }
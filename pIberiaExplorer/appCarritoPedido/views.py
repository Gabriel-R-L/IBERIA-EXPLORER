from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from appIberiaExplorer.models import AtributoPlan
from .models import *

from pIberiaExplorer.utils import APP_CARRITO_PEDIDO


###########################################
# CARRITO
###########################################
@login_required(login_url='/registro/')
def agregar_al_carrito(request, plan_id):
    # Verifica si el usuario ha confirmado su correo electrónico
    if not request.user.email_confirmed:
        context = {
            'mensaje_error': 'Verifique su cuenta para agregar planes al carrito.'
        }
        return render(request, 'appIberiaExplorer/index.html', context=context)
    
    # Obtiene el plan a agregar al carrito
    from appIberiaExplorer.models import Plan
    plan = get_object_or_404(Plan, id_plan_api=plan_id)
    
    # Obtiene o crea un carrito para el usuario actual
    cart, created = Carrito.objects.get_or_create(id_usuario=request.user)
    
    # Obtiene o crea un detalle de carrito para el plan específico
    carrito_details, created = CarritoDetalle.objects.get_or_create(id_carrito=cart, id_plan=plan, cantidad=1)
    
    if not created:
        # Si el detalle ya existía, incrementa la cantidad
        carrito_details.cantidad += 1
        carrito_details.save()
    
    return redirect('/carrito')


@login_required(login_url='/registro/')
def actualizar_carrito(request, detalle_id):
    # Obtiene el detalle del carrito para el usuario actual
    detalle = get_object_or_404(CarritoDetalle, id_carrito_detalle=detalle_id, id_carrito__id_usuario=request.user)
    
    if request.method == 'POST':
        # Actualiza la cantidad del detalle del carrito
        cantidad = int(request.POST['cantidad'])
        if cantidad > 0:
            detalle.cantidad = cantidad
            detalle.save()
        else:
            # Si la cantidad es 0 o menos, elimina el detalle del carrito
            detalle.delete()
    
    return redirect('/carrito')


def eliminar_del_carrito(request, detalle_id):
    # Obtiene el detalle del carrito para el usuario actual
    detalle = get_object_or_404(CarritoDetalle, id_carrito_detalle=detalle_id, id_carrito__id_usuario=request.user)
    
    if request.method == 'POST':
        # Elimina el detalle del carrito
        detalle.delete()
    
    return redirect('/carrito')


@login_required(login_url='/registro/')
def ver_carrito(request):
    # Obtiene el carrito para el usuario actual
    carrito = get_object_or_404(Carrito, id_usuario=request.user)
    
    # Obtiene los detalles del carrito
    carrito_details = CarritoDetalle.objects.filter(id_carrito=carrito)
    total = 0
    
    # Calcula el total del carrito
    for detail in carrito_details:
        total += detail.id_plan.precio * detail.cantidad
    if total % 1 == 0:
        total = int(total)
    
    # Verifica si hay algún pedido pendiente
    if Pedido.objects.filter(id_cliente=request.user, estado='PENDIENTE'):
        context = {
            'carrito': carrito,
            'detalles': carrito_details,
            'total': total,
            "pendiente": True,
        }
    else:
        context = {
            'carrito': carrito,
            'detalles': carrito_details,
            'total': total,
        }

    return render(request, f"{APP_CARRITO_PEDIDO}/carrito.html", context=context)


###########################################
# PEDIDOS
###########################################
@login_required(login_url='/registro/')
def completar_pedido(request, url_to_pay=0):
    # Obtiene el carrito para el usuario actual
    carrito = get_object_or_404(Carrito, id_usuario=request.user)
    
    # Obtiene los detalles del carrito
    carrito_details = CarritoDetalle.objects.filter(id_carrito=carrito)
    total = 0
    
    # Calcula el total del pedido
    for detail in carrito_details:
        total += detail.id_plan.precio * detail.cantidad
    if total % 1 == 0:
        total = int(total)
    
    if url_to_pay == 1:
        # Crea un nuevo pedido
        pedido = Pedido.objects.create(id_cliente=request.user, total=total)
    
        # Crea los detalles del pedido y guarda los atributos del plan en la sesión
        for detail in carrito_details:
            PedidoDetalle.objects.create(id_pedido=pedido, id_plan=detail.id_plan, cantidad=detail.cantidad)
            atributos_plan = AtributoPlan.objects.filter(plan=detail.id_plan).values_list('id_atributo_plan', flat=True)
            request.session['atributos_plan'] = list(atributos_plan)
            
    # Elimina el carrito actual y crea uno nuevo
    carrito.delete()
    nuevo_carrito = Carrito.objects.create(id_usuario=request.user)
    
    return redirect('/carrito/pagar_pedidos')


@login_required(login_url='/registro/')
def pagar_pedidos(request):
    # Obtiene todos los pedidos pendientes del usuario actual
    pedidos_pendientes = Pedido.objects.filter(id_cliente=request.user, estado='PENDIENTE')
    
    # Asigna el nombre del plan a cada pedido
    for pedido in pedidos_pendientes:
        detalle = PedidoDetalle.objects.filter(id_pedido=pedido).values_list('id_plan__titulo', flat=True).first()
        pedido.nombre_plan = detalle
            
    context = {
        'pedidos_pendientes': pedidos_pendientes,
    }
    
    # Renderiza la plantilla con el contexto
    return render(request, 'appCarritoPedido/pagar_pedidos.html', context)


@login_required(login_url='/registro/')
def completar_pago(request):
    from appNotificaciones.models import Notificacion
    from appAjustes.models import UsuarioPreferencia
    
    # Obtiene todos los pedidos pendientes del usuario actual
    pedidos = Pedido.objects.filter(id_cliente=request.user, estado='PENDIENTE')
    
    for pedido in pedidos:
        # Marca el pedido como completado
        pedido.estado = 'COMPLETADO'
        pedido.save()
        
        # Crea una notificación para el usuario
        pedido.nombre_plan = PedidoDetalle.objects.filter(id_pedido=pedido).first().id_plan.titulo
        notificacion = Notificacion.objects.create(
            usuario=request.user, 
            titulo_notificacion=f"¡Pedido del plan con título '{pedido.nombre_plan}' pagado!",
            mensaje_notificacion="Revise los detalles de su pedido en la sección de pedidos."
        )
    
        # Añade las preferencias del usuario basadas en los atributos del plan
        atributos = request.session.get('atributos_plan')
        for atributo_id in atributos:
            atributo_plan_instance = AtributoPlan.objects.get(id_atributo_plan=atributo_id)
            if not UsuarioPreferencia.objects.filter(usuario=request.user, atributo_plan=atributo_plan_instance).exists():
                UsuarioPreferencia.objects.create(usuario=request.user, atributo_plan=atributo_plan_instance)
    
    return redirect('/carrito/pagar_pedidos')


@login_required(login_url='/registro/')
def cancelar_pedido(request, pedido_id):
    # Obtiene el pedido y verifica que pertenece al usuario actual
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id, id_cliente=request.user)
    
    # Actualiza el estado del pedido a 'CANCELADO'
    pedido.estado = 'CANCELADO'
    pedido.save()
    
    return redirect('/carrito/pagar_pedidos')


@login_required(login_url='/registro/')
def ver_pedidos(request):
    # Obtiene todos los pedidos completados y cancelados del usuario actual
    pedidos_completados = Pedido.objects.filter(id_cliente=request.user, estado='COMPLETADO')
    pedidos_cancelados = Pedido.objects.filter(id_cliente=request.user, estado='CANCELADO')
    
    context = {
        'pedidos_completados': pedidos_completados,
        'pedidos_cancelados': pedidos_cancelados,
    }
    
    # Renderiza la plantilla con el contexto
    return render(request, 'appCarritoPedido/pedidos.html', context=context)


@login_required(login_url='/registro/')
def ver_pedido_detalle(request, pedido_id):
    # Obtiene el pedido y verifica que pertenece al usuario actual
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id, id_cliente=request.user)
    
    # Obtiene los detalles del pedido
    detalles = PedidoDetalle.objects.filter(id_pedido=pedido)
    
    total = 0
    for detail in detalles:
        total += detail.id_plan.precio * detail.cantidad
    if total % 1 == 0:
        total = int(total)
    
    context = {
        'pedido': pedido,
        'detalles': detalles,
        'total': total,
    }
    
    # Renderiza la plantilla con el contexto
    return render(request, 'appCarritoPedido/pedido_detalle.html', context)

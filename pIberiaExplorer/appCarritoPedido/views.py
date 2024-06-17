from multiprocessing import context
from django.shortcuts import redirect, render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from appIberiaExplorer.models import AtributoPlan
from .models import *

from pIberiaExplorer.utils import APP_CARRITO_PEDIDO


###########################################
# CARRITO
###########################################
@login_required(login_url='/registro/')
def agregar_al_carrito(request, plan_id):
    if not request.user.email_confirmed:
        context = {
            'mensaje_error': 'Verifique su correo electrónico para agregar planes al carrito.'
        }
        return render(request, 'appIberiaExplorer/index.html', context=context)
    from appIberiaExplorer.models import Plan
    print(">>>>>>>>>>>>>>>>>>", plan_id)
    plan = get_object_or_404(Plan, id_plan_api=plan_id)
    cart, created = Carrito.objects.get_or_create(id_usuario=request.user)
    carrito_details, created = CarritoDetalle.objects.get_or_create(id_carrito=cart, id_plan=plan, cantidad=1)
    
    if not created:
        carrito_details.cantidad += 1
        carrito_details.save()
    
    return redirect('/carrito')

@login_required(login_url='/registro/')
def actualizar_carrito(request, detalle_id):
    detalle = get_object_or_404(CarritoDetalle, id_carrito_detalle=detalle_id, id_carrito__id_usuario=request.user)
    
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
        if cantidad > 0:
            detalle.cantidad = cantidad
            detalle.save()
        else:
            detalle.delete()  # Si la cantidad es 0 o menos, elimina el detalle del carrito
    
    return redirect('/carrito')


def eliminar_del_carrito(request, detalle_id):
    detalle = get_object_or_404(CarritoDetalle, id_carrito_detalle=detalle_id, id_carrito__id_usuario=request.user)
    
    if request.method == 'POST':
        detalle.delete()
    
    return redirect('/carrito')
    

@login_required(login_url='/registro/')
def ver_carrito(request):
    carrito = get_object_or_404(Carrito, id_usuario=request.user)
    carrito_details = CarritoDetalle.objects.filter(id_carrito=carrito)
    total = 0
    
    for detail in carrito_details:
        total += detail.id_plan.precio * detail.cantidad
    if total % 1 == 0:
        total = int(total)
    
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
    carrito = get_object_or_404(Carrito, id_usuario=request.user)
    
    carrito_details = CarritoDetalle.objects.filter(id_carrito=carrito)
    total = 0
    
    for detail in carrito_details:
        total += detail.id_plan.precio * detail.cantidad
    if total % 1 == 0:
            total = int(total)
    
    if url_to_pay == 1:
        pedido = Pedido.objects.create(id_cliente=request.user, total=total)
    
        for detail in carrito_details:
            PedidoDetalle.objects.create(id_pedido=pedido, id_plan=detail.id_plan, cantidad=detail.cantidad)
            # Atributos plan para asigna en foreign key
            atributos_plan = AtributoPlan.objects.filter(plan=detail.id_plan).values_list('id_atributo_plan', flat=True)
            request.session['atributos_plan'] = list(atributos_plan)
            
    carrito.delete()
    nuevo_carrito = Carrito.objects.create(id_usuario=request.user)
    
    return redirect('/carrito/pagar_pedidos')


@login_required(login_url='/registro/')
def pagar_pedidos(request):
    # Obtener todos los pedidos pendientes del usuario actual
    pedidos_pendientes = Pedido.objects.filter(id_cliente=request.user, estado='PENDIENTE')
    
    for pedido in pedidos_pendientes:
        detalle = PedidoDetalle.objects.filter(id_pedido=pedido).values_list('id_plan__titulo', flat=True).first()
        pedido.nombre_plan = detalle
            
    # Preparar el contexto para pasar a la plantilla
    context = {
        'pedidos_pendientes': pedidos_pendientes,
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'appCarritoPedido/pagar_pedidos.html', context)


@login_required(login_url='/registro/')
def completar_pago(request):
    from appNotificaciones.models import Notificacion
    from appAjustes.models import UsuarioPreferencia
    pedidos = Pedido.objects.filter(id_cliente=request.user, estado='PENDIENTE')
    
    for pedido in pedidos:
        pedido.estado = 'COMPLETADO'
        pedido.save()
        
        notificacion = Notificacion.objects.create(
                                usuario=request.user, 
                                titulo_notificacion=f"¡Pedido {pedido} pagado!",
                                mensaje_notificacion="Revise los detalles de su pedido en la sección de pedidos.")
    
        atributos =  request.session.get('atributos_plan')
        for atributo_id in atributos:
            atributo_plan_instance = AtributoPlan.objects.get(id_atributo_plan=atributo_id)

            if not UsuarioPreferencia.objects.filter(usuario=request.user, atributo_plan=atributo_plan_instance).exists():
                usuario_preferencia = UsuarioPreferencia.objects.create(
                    usuario=request.user, 
                    atributo_plan=atributo_plan_instance)
    
    return redirect('/carrito/pagar_pedidos')


@login_required(login_url='/registro/')
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id, id_cliente=request.user)
    
    # Actualizar el estado del pedido a 'CANCELADO'
    pedido.estado = 'CANCELADO'
    pedido.save()
    
    return redirect('/carrito/pagar_pedidos')
    

@login_required(login_url='/registro/')
def ver_pedidos(request):
    # Obtener todos los pedidos completados y cancelados del usuario actual
    pedidos_completados = Pedido.objects.filter(id_cliente=request.user, estado='COMPLETADO')
    pedidos_cancelados = Pedido.objects.filter(id_cliente=request.user, estado='CANCELADO')
    
    context = {
        'pedidos_completados': pedidos_completados,
        'pedidos_cancelados': pedidos_cancelados,
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'appCarritoPedido/pedidos.html', context=context)


@login_required(login_url='/registro/')
def ver_pedido_detalle(request, pedido_id):
    # Obtener el pedido y verificar que pertenece al usuario actual
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id, id_cliente=request.user)
    
    # Obtener los detalles del pedido
    detalles = PedidoDetalle.objects.filter(id_pedido=pedido)
    
    total = 0
    for detail in detalles:
        total += detail.id_plan.precio  * detail.cantidad
    if total % 1 == 0:
        total = int(total)
    
    # Preparar el contexto para pasar a la plantilla
    context = {
        'pedido': pedido,
        'detalles': detalles,
        'total': total,
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'appCarritoPedido/pedido_detalle.html', context)
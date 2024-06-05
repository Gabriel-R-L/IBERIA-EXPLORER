from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from django.conf import settings
from django.db import IntegrityError

from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.core.mail import send_mail

import os
import sys
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


from datetime import timezone
import urllib.request as urllib

from .models import *

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from spanlp.palabrota import Palabrota
from django.utils.crypto import get_random_string

from api.Plantilla_API_Com_Madrid import obtener_datos_api

from django.core.paginator import Paginator

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt

from django.contrib.auth.decorators import login_required

from pIberiaExplorer.utils import APP_CARRITO_PEDIDO


###########################################
# Carrito
@login_required
def agregar_al_carrito(request, plan_id):
    from appIberiaExplorer.models import Plan
    plan = get_object_or_404(Plan, id=plan_id)
    cart, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_details, created = CarritoDetalle.objects.get_or_create(id_carrito=cart, plan=plan)
    
    if not created:
        carrito_details.cantidad += 1
        carrito_details.save()
    
    return redirect('/carrito')

@login_required
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
    

@login_required
def ver_carrito(request):
    carrito = get_object_or_404(Carrito, id_usuario=request.user)
    
    if carrito:
        carrito_details = CarritoDetalle.objects.filter(id_carrito=carrito)
        total = 0
        
        for detail in carrito_details:
            total += detail.id_plan.precio * detail.cantidad
            
        context = {
            'carrito': carrito,
            'detalles': carrito_details,
            'total': total,
        }
        
    else:
        context = {
            'carrito': None,
            'detalles': None,
            'total': 0,
        }

    return render(request, f"{APP_CARRITO_PEDIDO}/carrito.html", context=context)



###########################################
# Pedidos
@login_required
def completar_pedido(request):
    carrito = get_object_or_404(Carrito, id_usuario=request.user)
    carrito_details = CarritoDetalle.objects.filter(id_carrito=carrito)
    
    total = 0
    for detail in carrito_details:
        total += detail.id_plan.precio  * detail.cantidad
    
    pedido = Pedido.objects.create(id_cliente=request.user, total=total)
    
    for detail in carrito_details:
        PedidoDetalle.objects.create(id_pedido=pedido, id_plan=detail.id_plan, cantidad=detail.cantidad)
    
    carrito.delete()
    nuevo_carrito = Carrito.objects.create(id_usuario=request.user)
    
    return redirect('/carrito/pagar_pedidos')


@login_required
def pagar_pedidos(request):
    # Obtener todos los pedidos pendientes del usuario actual
    pedidos_pendientes = Pedido.objects.filter(id_cliente=request.user, estado='PENDIENTE')
    
    # Preparar el contexto para pasar a la plantilla
    context = {
        'pedidos_pendientes': pedidos_pendientes,
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'appCarritoPedido/pagar_pedidos.html', context)


@login_required
def completar_pago(request):
    pedidos = Pedido.objects.filter(id_cliente=request.user, estado='PENDIENTE')
    
    for pedido in pedidos:
        pedido.estado = 'COMPLETADO'
        pedido.save()
    
    return redirect('/carrito/pagar_pedidos')


@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id, id_cliente=request.user)
    
    # Actualizar el estado del pedido a 'CANCELADO'
    pedido.estado = 'CANCELADO'
    pedido.save()
    
    return redirect('/carrito/pagar_pedidos')
    

@login_required
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


@login_required
def ver_pedido_detalle(request, pedido_id):
    # Obtener el pedido y verificar que pertenece al usuario actual
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id, id_cliente=request.user)
    
    # Obtener los detalles del pedido
    detalles = PedidoDetalle.objects.filter(id_pedido=pedido)
    
    total = 0
    for detail in detalles:
        total += detail.id_plan.precio  * detail.cantidad
    
    # Preparar el contexto para pasar a la plantilla
    context = {
        'pedido': pedido,
        'detalles': detalles,
        'total': total,
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'appCarritoPedido/pedido_detalle.html', context)
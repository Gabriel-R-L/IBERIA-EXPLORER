from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404

from .models import *
from pIberiaExplorer.utils import APP_NOTIFICACIONES


##########################################
# NOTIFICACIONES
##########################################
def ver_notificaciones(request):
    user = request.user
    
    if Notificacion.objects.filter(usuario=user).exists():
        notificaciones = Notificacion.objects.filter(usuario=user, leido=False)
        notificaciones_no_leidas = list(notificaciones)
    else:
        notificaciones_no_leidas = None
    
    context = {
        "notificaciones": notificaciones_no_leidas,
    }
    
    return render(request, f'{APP_NOTIFICACIONES}/notificaciones.html', context=context)


##########################################
# VER NOTIFICACION
##########################################
def ver_notificacion(request, id):
    notificacion = get_object_or_404(Notificacion, usuario=request.user, id=id)
   
    context = {
        "notificacion": notificacion,
    }
    
    if notificacion.leido == False:
        notificacion.leido = True
        notificacion.save()
        
    return render(request, f'{APP_NOTIFICACIONES}/ver_notificacion.html', context=context)


##########################################
# BORRAR NOTIFICACIONES
##########################################
def eliminar_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    notificaciones.delete()
    
    return redirect('/notificaciones')


##########################################
# BORRAR NOTIFICACION
##########################################
def eliminar_notificacion(request, id):
    notificacion = get_object_or_404(Notificacion, usuario=request.user, id=id)
    notificacion.delete()
    
    return redirect('/notificaciones')

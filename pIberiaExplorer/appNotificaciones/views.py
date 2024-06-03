from django.shortcuts import render
from requests import get
from .models import Notificacion
from django.shortcuts import redirect, render, get_object_or_404

from pIberiaExplorer.utils import APP_NOTIFICACIONES


##########################################
# Notificaciones
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
# Ver notificacion
def ver_notificacion(request, id):
    notificacion = get_object_or_404(Notificacion, usuario=request.user, id=id)
   
    context = {
        "detalles_notificacion": notificacion,
    }
    
    if notificacion.leido == False:
        notificacion.leido = True
        notificacion.save()
        
    return render(request, f'{APP_NOTIFICACIONES}/ver_notificacion.html', context=context)


##########################################
# Borrar todas las notificaciones
def eliminar_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    notificaciones.delete()
    
    return redirect('/notificaciones')


##########################################
# Borrar notificacion
def eliminar_notificacion(request, id):
    notificacion = get_object_or_404(Notificacion, usuario=request.user, id=id)
    notificacion.delete()
    
    return redirect('/notificaciones')

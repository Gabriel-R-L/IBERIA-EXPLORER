from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404

from .models import *
from pIberiaExplorer.utils import APP_NOTIFICACIONES


##########################################
# NOTIFICACIONES
##########################################
def ver_notificaciones(request):
    """
    Vista para mostrar todas las notificaciones no leídas de un usuario.

    - Obtiene el usuario actualmente autenticado.
    - Filtra las notificaciones no leídas asociadas a ese usuario.
    - Prepara el contexto con las notificaciones no leídas.
    - Renderiza la plantilla 'notificaciones.html' con el contexto.

    Returns:
        - Renderiza la plantilla de notificaciones con las notificaciones no leídas.
    """
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
    """
    Vista para mostrar los detalles de una notificación específica.

    - Recupera la notificación específica usando su ID y el usuario autenticado.
    - Marca la notificación como leída si aún no lo está.
    - Prepara el contexto con la notificación para mostrar sus detalles.
    - Renderiza la plantilla 'ver_notificacion.html' con el contexto.

    Args:
        id (int): El ID de la notificación que se quiere ver.

    Returns:
        - Renderiza la plantilla de ver notificación con los detalles de la notificación.
    """
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
    """
    Vista para eliminar todas las notificaciones de un usuario.

    - Obtiene todas las notificaciones asociadas al usuario autenticado.
    - Elimina todas las notificaciones encontradas.
    - Redirige al usuario de nuevo a la página de notificaciones.

    Returns:
        - Redirige a la página de notificaciones después de eliminar las notificaciones.
    """
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    notificaciones.delete()
    
    return redirect('/notificaciones')


##########################################
# BORRAR NOTIFICACION
##########################################
def eliminar_notificacion(request, id):
    """
    Vista para eliminar una notificación específica.

    - Recupera la notificación específica usando su ID y el usuario autenticado.
    - Elimina la notificación encontrada.
    - Redirige al usuario de nuevo a la página de notificaciones.

    Args:
        id (int): El ID de la notificación que se quiere eliminar.

    Returns:
        - Redirige a la página de notificaciones después de eliminar la notificación.
    """
    notificacion = get_object_or_404(Notificacion, usuario=request.user, id=id)
    notificacion.delete()
    
    return redirect('/notificaciones')

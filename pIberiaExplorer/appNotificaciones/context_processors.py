from .models import Notificacion

def unread_notifications(request):
    cantidad_notificaciones = 0
    if request.user.is_authenticated:
        cantidad_notificaciones = Notificacion.objects.filter(usuario=request.user, leido=False).count()
        
    context = {
        'cantidad_notificaciones': cantidad_notificaciones
    }
    return context
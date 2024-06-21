from .models import Notificacion


# Función para añadir el contexto de las notificaciones
def unread_notifications(request):
    cantidad_notificaciones = 0
    # Si el usuario está autenticado, se obtiene la cantidad de notificaciones no leídas
    if request.user.is_authenticated:
        cantidad_notificaciones = Notificacion.objects.filter(usuario=request.user, leido=False).count()
        
    context = {
        'cantidad_notificaciones': cantidad_notificaciones
    }
    return context
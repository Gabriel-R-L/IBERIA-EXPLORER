from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail

from .views import prepararEmail
from services.send_mail import prepararEmail
from .models import Notificacion


@receiver(user_logged_in)
def send_login_email(request, user, **kwargs):
    prepararEmail(
                    user.email,
                    "Inicio de sesión",
                    f"Tu cuenta '@{user.username}' ha iniciado sesión en un dispositivo.\n\nSi no has sido tú, por favor, comuníquese con nosotros.",
                )
    
    if user.email_confirmed == False:
        notificacion = Notificacion.objects.create(
            usuario=user
            , titulo_notificacion=f"Confirma tu cuenta."
            , mensaje_notificacion="Por favor, revise su correo para verificar su cuenta.")
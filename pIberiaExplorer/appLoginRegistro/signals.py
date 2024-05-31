from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail

from .views import prepararEmail
from services.send_mail import prepararEmail


@receiver(user_logged_in)
def send_login_email(request, user, **kwargs):
    prepararEmail(
                    user.email,
                    "Inicio de sesión",
                    f"Tu cuenta '@{user.username}' ha iniciado sesión en un dispositivo.\n\nSi no has sido tú, por favor, comuníquese con nosotros.",
                )
from re import DEBUG
from django.conf import settings

from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.core.mail import send_mail

from appLoginRegistro.models import Usuario


##########################################
# Preparar email
##########################################
def prepararEmail(email, asunto, mensaje):
    """
    Prepara y envía un correo electrónico.

    Args:
        email (str): Dirección de correo electrónico del destinatario.
        asunto (str): Asunto del correo electrónico.
        mensaje (str): Contenido del correo electrónico.

    Returns:
        None
    """
    asunto = f"{asunto}"
    mensaje = f"{mensaje}"
    enviarEmail(email, asunto, mensaje)


##########################################
# Enviar email
##########################################
def enviarEmail(email, asunto, mensaje):
    """
    Envía un correo electrónico usando las configuraciones de Django.

    Args:
        email (str): Dirección de correo electrónico del destinatario.
        asunto (str): Asunto del correo electrónico.
        mensaje (str): Contenido del correo electrónico.

    Returns:
        None
    """
    sender = settings.EMAIL_HOST_USER  # Email del remitente configurado en settings
    recipient = [email]  # Lista de destinatarios

    send_mail(
        asunto,
        mensaje,
        sender,
        recipient,
        fail_silently=False,  # No silenciar errores para que se lancen excepciones si hay problemas
        html_message=mensaje,  # Mensaje en formato HTML
    )


##########################################
# Validacion correo
##########################################
def validarEmail(correo):
    """
    Valida si una dirección de correo electrónico es válida y si no está duplicada en la base de datos.

    Args:
        correo (str): Dirección de correo electrónico a validar.

    Returns:
        bool: True si el correo es válido y no está duplicado, False en caso contrario.
    """
    try:
        email_validated = validate_email(correo)  # Validación sintáctica del correo

        existe_correo_db = Usuario.objects.filter(email=correo).exists()  # Verificación si el correo ya está en la base de datos

        if not DEBUG:  # Si no estamos en modo DEBUG
            if existe_correo_db or not email_validated:  # Si el correo existe en la base de datos o no es válido sintácticamente
                return False
            else:
                return True

        if DEBUG:  # Si estamos en modo DEBUG
            return email_validated  # Devolver el resultado de la validación sintáctica del correo

    except ValidationError:
        return False  # Manejar excepción si la validación de correo falla
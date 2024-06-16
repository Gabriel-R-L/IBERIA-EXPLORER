from re import DEBUG
from django.conf import settings

from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.core.mail import send_mail

from appLoginRegistro.models import Usuario


##########################################
# Preparar email
def prepararEmail(email, asunto, mensaje):
    asunto = f"{asunto}"
    mensaje = f"{mensaje}"
    enviarEmail(email, asunto, mensaje)


##########################################
# Enviar email
def enviarEmail(email, asunto, mensaje):
    sender = settings.EMAIL_HOST_USER  # emisor
    recipient = [email]  # receptor

    send_mail(
        asunto,
        mensaje,
        sender,
        recipient,
        fail_silently=False,
        html_message=mensaje,
    )


##########################################
# Validacion correo
def validarEmail(correo):
    try:
        email_validated = validate_email(correo)
        existe_correo_db = Usuario.objects.filter(email=correo).exists()


        ##########################################
        # DEBUG FALSE
        ##########################################
        # Si existe el correo o la sintaxis del correo no es adecuada
        if not DEBUG:
            if existe_correo_db or not validate_email:
                return False
            else:
                return True

        ##########################################
        # DEBUG TRUE
        ##########################################
        if DEBUG:
            return email_validated

    except ValidationError:
        return False

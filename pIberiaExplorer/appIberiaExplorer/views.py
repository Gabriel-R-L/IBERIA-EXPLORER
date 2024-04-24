from django.shortcuts import redirect, render
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

from .forms import *
from .models import *

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from spanlp.palabrota import Palabrota
from django.utils.crypto import get_random_string

from api.Plantilla_API_Com_Madrid import obtener_datos_api


###########################################
# (API) Actividades y eventos de Ayto. Madrid
##########################################
def resultado_datos_api(request):
    datos = obtener_datos_api()
    datos_totales = len(datos)
    
    context = {
        "datos": datos,
        "datos_totales": datos_totales,
    }
    return render(request, "actividades_&_eventos_ayto_madrid.html", context=context)


###########################################
# Index
##########################################
def index(request):
    return render(request, "index.html")


##########################################
# Iniciar sesión
##########################################
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                try:
                    user = Usuario.objects.get(email=request.POST["email"])

                    print(user.email)

                    if (
                        user is not None
                        and user.is_superuser == False
                        and user.is_staff == False
                        and user.is_active == True
                        and user.fecha_baja == None
                    ):
                        login_user(request, user)

                        prepararEmail(
                            request.user.email,
                            "Inicio de sesión",
                            f"Tu cuenta '@{request.user.username}' ha iniciado sesión en un dispositivo.\n\nSi no has sido tú, por favor, comuníquese con nosotros.",
                        )

                        return redirect("/")

                    else:
                        context = {
                            "form": LoginForm(),
                            "mensaje_error": "El usuario y/o contraseña son incorrectos",
                            "sub_mensaje_error": "Por favor, verifique que el nombre de usuario y la contraseña sean correctos.",
                        }
                        return render(request, "login.html", context=context)
                except:
                    print("Error inesperado")

                    context = {
                        "form": LoginForm(),
                        "mensaje_error": "Ha habido un error inesperado",
                        "sub_mensaje_error": "Por favor, inténtelo de nuevo más tarde.",
                    }
                    return render(request, "login.html", context=context)

            else:
                print("La contraseña no coincide con el hash almacenado")
                context = {
                    "form": LoginForm(),
                    "mensaje_error": "Ha habido un error inesperado",
                    "sub_mensaje_error": "Por favor, inténtelo de nuevo más tarde.",
                }

                return render(request, "login.html", context=context)
        except ValidationError:
            context = {
                "form": LoginForm(),
                "mensaje_error": "Ha habido un error inesperado",
                "sub_mensaje_error": "Por favor, inténtelo de nuevo más tarde.",
            }
            return render(request, "login.html", context=context)
    else:
        context = {"form": LoginForm()}

        return render(request, "login.html", context=context)


##########################################
# Crear cuenta
##########################################
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        try:
            if form.is_valid():
                if validarEmail(request.POST["email"]):
                    if request.POST["password"] == request.POST["password_confirm"]:
                        # Comprobar que no se ha escrito una mala palabra
                        palabrota = Palabrota()
                        if palabrota.contains_palabrota(request.POST["username"]):
                            context = {
                                "mensaje_error": "Nombre inapropiado",
                                "sub_mensaje_error": "Por favor, elija un nombre de usuario adecuado.",
                                "form": RegisterForm(),
                            }

                            return render(request, "register.html", context=context)

                        # Creo el usuario
                        user = Usuario.objects.create(
                            username=request.POST["username"],
                            email=request.POST["email"],
                            password=request.POST["password"],
                            confirmation_token=get_random_string(length=32),
                        )
                        user.save()

                        print(f"Token: {user.confirmation_token}")

                        # genera el enlace de confirmación
                        confirmation_link = request.build_absolute_uri(
                            reverse(
                                "appIberiaExplorer:confirm_email",
                                args=[user.confirmation_token],
                            )
                        )

                        print("Link: {confirmation_link}")

                        # ip = buscarIP()
                        login_user(request, user)

                        # Envio correo
                        mensaje = f"Bienvenido a nuestra plataforma Iberia Explorer.<br>Por favor confirma tu correo electrónico haciendo clic en el siguiente enlace:<br>{confirmation_link}"

                        prepararEmail(
                            user.email,
                            f"¡Bienvenido, { user.username }!",
                            mensaje,
                        )

                        return redirect("/")
                    else:
                        context = {
                            "mensaje_error": "Las contraseñas no coinciden",
                            "sub_mensaje_error": "Por favor, verifique que las contraseñas coincidan.",
                            "form": RegisterForm(),
                        }

                        return render(request, "register.html", context=context)
                else:
                    context = {
                        "mensaje_error": "El email ya existe en la base de datos o no existe",
                        "sub_mensaje_error": "Pruebe con otro correo, o inicie sesión.",
                        "form": RegisterForm(),
                    }

                    return render(request, "register.html", context=context)
            else:
                context = {
                    "mensaje_error": "El email ya existe en la base de datos o no existe",
                    "sub_mensaje_error": "Pruebe con otro correo, o inicie sesión.",
                    "form": RegisterForm(),
                }

                return render(request, "register.html", context=context)

        except IntegrityError:
            context = {
                "mensaje_error": "El usuario ya existe",
                "sub_mensaje_error": "Pruebe con otro correo, o inicie sesión.",
                "form": RegisterForm(),
            }

            return render(request, "register.html", context=context)
    else:
        context = {
            "form": RegisterForm(),
        }

        return render(request, "register.html", context=context)


##########################################
# Cerrar sesión
##########################################
def logout(request):
    logout_user(request)

    context = {
        "form": LoginForm(),
    }

    return redirect("/login", context=context)


##########################################
# Borrar cuenta (borrado lógico)
##########################################
def delete_account(request):
    usuario = request.user.usuario
    usuario.activo = False
    usuario.fecha_baja = timezone.now()
    usuario.save()

    prepararEmail(
        request.user.email,
        "Tu cuenta ha sido eliminada",
        f"Tu cuenta '@{request.user.username}' ha sido eliminada. No podrás iniciar sesión en nuestra plataforma.\n\nSi crees que se trata de un error, por favor, comuníquese con nosotros.",
    )

    logout_user(request)

    return redirect("/")


##########################################
# Preparar email
##########################################
def prepararEmail(email, asunto, mensaje):
    asunto = f"{asunto}"
    mensaje = f"{mensaje}"
    enviarEmail(email, asunto, mensaje)


##########################################
# Enviar email
##########################################
def enviarEmail(email, asunto, mensaje):
    sender = settings.EMAIL_HOST_USER  # emisor
    recipient = [email]  # receptor

    print(f"Email: {email},\n Asunto: {asunto},\n Mensaje: {mensaje}")

    send_mail(
        asunto,
        mensaje,
        sender,
        recipient,
        fail_silently=False,
        html_message=mensaje,
    )


##########################################
# Verificar email
##########################################
def confirm_email(request, token):
    try:
        user = Usuario.objects.get(confirmation_token=token)
        user.email_confirmed = True
        user.save()
        return redirect("/email_confirmed")
    except Usuario.DoesNotExist:
        context = {
            "mensaje_error": "El token de confirmación es inválido",
            "sub_mensaje_error": "Por favor, verifique que el enlace sea correcto.",
        }
        return redirect("/", context=context)


##########################################
# Email confirmado
##########################################
def email_confirmed(request):
    return render(request, "email_confirmed.html")


##########################################
# Validacion correo
##########################################
def validarEmail(correo):
    try:
        email_exists = validate_email(correo)
        existe_correo_db = Usuario.objects.filter(email=correo).exists()

        #!#########################################
        #! DEBUG FALSE
        #!#########################################
        # Si existe el correo o la sintaxis del correo no es adecuada
        # if existe_correo_db or not validate_email:
        #     print("El correo no es válido")
        #     return False
        # else:
        #     return True

        #!#########################################
        #! DEBUG TRUE
        #!#########################################

        print(f"!!!!!!!!! {email_exists}")

        return email_exists

    except ValidationError:
        return False


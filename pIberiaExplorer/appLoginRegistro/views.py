import re
from turtle import ht
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from django.conf import settings
from django.db import IntegrityError

from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.core.mail import send_mail

from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string

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

from api.Datos_API_Com_Madrid import obtener_datos_api

from django.core.paginator import Paginator

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt

from django.contrib.auth.decorators import login_required

from services.send_mail import prepararEmail, validarEmail
from services.buscar_ip import buscar_ip
from pIberiaExplorer.utils import APP_LOGIN_REGISTRO
from appCarritoPedido.views import Carrito, Pedido

from appNotificaciones.models import Notificacion


###########################################
# Login/Registro
def login_register(request):
    """ 
        - Método para crear cuenta o iniciar sesión.
            - Se buscará en la base de datos si el usuario existe.
                - Si existe:
                    - Se comprobará si la cuenta es creada manualmente o con Google.
                    - Se comprobará si la cuenta está activa.
                    - Se iniciará sesión siempre y cuando se cumplan las condiciones previstas.
                    - Se enviará un correo sobre el nuevo inicio de sesión.
                - Si no existe:
                    - Se comprobará que el usuario no esté autenticado en la aplicación.
                        - Si lo está, se redirigirá a la página principal.
                        - Si no lo está:
                            - Se creará la cuenta llamando al método Register()
                    
        · Params: 
            - None
            
        Returns:
            - None
    """
    
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(request, f"{APP_LOGIN_REGISTRO}/login_register.html", context={"form": LoginRegisterForm()})
        
    if request.method == "POST":
        email_to_verify = request.POST["email"]
        user_has_account = Usuario.objects.filter(email=email_to_verify).first()
        request.session["email"] = email_to_verify
        if user_has_account:
            return redirect("/registro/login")
        else:
            return redirect("/registro/register")
           

##########################################
# Iniciar sesión
def login(request):
    if request.method == "POST":
        email_to_find = request.session.get("email", None)
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                try:
                    user = get_object_or_404(Usuario, email=email_to_find)
                    if (
                        user is not None
                        and user.is_superuser == False
                        and user.is_staff == False
                        and user.is_active == True
                        and user.fecha_baja == None
                    ):
                        login_user(request, user, backend="django.contrib.auth.backends.ModelBackend")
                        
                        prepararEmail(
                            user.email,
                            "Inicio de sesión",
                            f"Tu cuenta '{user.username}' ha iniciado sesión en un dispositivo con IP {buscar_ip()}.\n\nSi no has sido tú, por favor, contáctenos a este correo.",
                        )

                        return redirect("/")
                    else:
                        print("El usuario no existe o no está activo")
                        context = {
                            "form": LoginForm(),
                            "mensaje_error": "El usuario y/o contraseña son incorrectos",
                            "sub_mensaje_error": "Por favor, verifique que el nombre de usuario y la contraseña sean correctos.",
                        }
                        return render(request, f"{APP_LOGIN_REGISTRO}/login.html", context=context)
                except:
                    print("Ha habido un error inesperado")
                    context = {
                        "form": LoginForm(),
                        "mensaje_error": "Ha habido un error inesperado",
                        "sub_mensaje_error": "Por favor, inténtelo de nuevo más tarde.",
                    }
                    return render(request, f"{APP_LOGIN_REGISTRO}/login.html", context=context)

            else:
                print("La contraseña no coincide con el hash almacenado")
                context = {
                    "form": LoginForm(),
                    "mensaje_error": "Ha habido un error inesperado",
                    "sub_mensaje_error": "Por favor, inténtelo de nuevo más tarde.",
                }

                return render(request, f"{APP_LOGIN_REGISTRO}/login.html", context=context)
        except ValidationError:
            context = {
                "form": LoginForm(),
                "mensaje_error": "Ha habido un error inesperado",
                "sub_mensaje_error": "Por favor, inténtelo de nuevo más tarde.",
            }
            return render(request, f"{APP_LOGIN_REGISTRO}/login.html", context=context)
    else:
        context = {"form": LoginForm()}
        return render(request, f"{APP_LOGIN_REGISTRO}/login.html", context=context)


##########################################
# Crear cuenta
def register(request):
    if request.method == "POST":
        email = request.session.get("email", None)
        form = RegisterForm(request.POST)
        try:
            if form.is_valid():
                if validarEmail(email):
                    if request.POST["password"] == request.POST["password_confirm"]:
                        # Comprobar que no se ha escrito una mala palabra
                        palabrota = Palabrota()
                        if palabrota.contains_palabrota(request.POST["username"]):
                            context = {
                                "mensaje_error": "Nombre inapropiado",
                                "sub_mensaje_error": "Por favor, elija un nombre de usuario adecuado.",
                                "form": RegisterForm(),
                            }

                            return render(request, f"{APP_LOGIN_REGISTRO}/register.html", context=context)

                        # Creo el usuario
                        user = Usuario.objects.create(
                            username=request.POST["username"],
                            email=email,
                            password=request.POST["password"],
                            confirmation_token=get_random_string(length=32),
                        )
                        user.save()
                        
                        notificacion = Notificacion.objects.create(
                              usuario=user
                            , titulo_notificacion=f"¡Bienvenido {user.username}!"
                            , mensaje_notificacion="Por favor, revise su correo para verificar su cuenta.")
                        
                        notificacion2 = Notificacion.objects.create(
                              usuario=user
                            , titulo_notificacion=f"Configura tu cuenta"
                            , mensaje_notificacion="Recuerda que puedes configurar tu cuenta en la sección de 'Mi perfil', y personalizar tu experiencia en nuestra plataforma.")
                        
                        carrito_usuario = Carrito.objects.create(id_usuario=user)
                        carrito_usuario.save()
                        pedido_usuario = Pedido.objects.create(id_cliente=user, total=0, fecha_reserva=timezone.now())
                        pedido_usuario.save()

                        # Genera el enlace de confirmación
                        confirmation_link = request.build_absolute_uri(
                            reverse(
                                f"{APP_LOGIN_REGISTRO}:confirm_email",
                                args=[user.confirmation_token],
                            )
                        )
                        
                        if (
                        user is not None
                        and user.is_superuser == False
                        and user.is_staff == False
                        and user.is_active == True
                        and user.fecha_baja == None
                        ):
                            login_user(request, user, backend="django.contrib.auth.backends.ModelBackend")

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

                        return render(request, f"{APP_LOGIN_REGISTRO}/register.html", context=context)
                else:
                    context = {
                        "mensaje_error": "El email ya existe en la base de datos o no existe",
                        "sub_mensaje_error": "Pruebe con otro correo, o inicie sesión.",
                        "form": RegisterForm(),
                    }

                    return render(request, f"{APP_LOGIN_REGISTRO}/register.html", context=context)
            else:
                context = {
                    "mensaje_error": "El email ya existe en la base de datos o no existe",
                    "sub_mensaje_error": "Pruebe con otro correo, o inicie sesión.",
                    "form": RegisterForm(),
                }

                return render(request, f"{APP_LOGIN_REGISTRO}/register.html", context=context)

        except IntegrityError:
            context = {
                "mensaje_error": "El usuario ya existe",
                "sub_mensaje_error": "Pruebe con otro correo, o inicie sesión.",
                "form": RegisterForm(),
            }

            return render(request, f"{APP_LOGIN_REGISTRO}/register.html", context=context)
    else:
        context = {
            "form": RegisterForm(),
        }

        return render(request, f"{APP_LOGIN_REGISTRO}/register.html", context=context)


##########################################
# Cerrar sesión
@login_required(login_url='/registro/')
def logout(request):
    logout_user(request)

    context = {
        "form": LoginRegisterForm(),
    }

    return redirect("/registro", context=context)

@login_required(login_url='/registro/')
def logout_confirmation(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(f'{APP_LOGIN_REGISTRO}/logout_confirmation.html', {}, request=request)
        return JsonResponse({'html': html})
    return render(request, f"{APP_LOGIN_REGISTRO}/logout_confirmation.html")


##########################################
# Borrar cuenta (borrado lógico)
@login_required(login_url='/registro/')
def delete_account(request):
    usuario = request.user
    usuario.activo = False
    usuario.fecha_baja = timezone.now()
    usuario.is_active = False
    usuario.save()

    prepararEmail(
        request.user.email,
        "Tu cuenta ha sido eliminada",
        f"Tu cuenta '{request.user.username}' ha sido eliminada. No podrás iniciar sesión en nuestra plataforma.\n\nSi crees que se trata de un error, por favor, comuníquese con nosotros.",
    )

    logout_user(request)

    return redirect("/")
    
@login_required(login_url='/registro/')
def delete_account_confirmation(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(f'{APP_LOGIN_REGISTRO}/delete_account_confirmation.html', {}, request=request)
        return JsonResponse({'html': html})
    return render(request, f"{APP_LOGIN_REGISTRO}/delete_account_confirmation.html")


##########################################
# Verificar email
@login_required(login_url='/registro/')
def confirm_email(request, token):
    try:
        user = Usuario.objects.get(confirmation_token=token)
        user.email_confirmed = True
        user.save()
        return redirect("/registro/email_confirmed")
    except Usuario.DoesNotExist:
        context = {
            "mensaje_error": "El token de confirmación es inválido",
            "sub_mensaje_error": "Por favor, verifique que el enlace sea correcto.",
        }
        return redirect("/", context=context)


##########################################
# Email confirmado
@login_required(login_url='/registro/')
def email_confirmed(request):
    return render(request, f"{APP_LOGIN_REGISTRO}/email_confirmed.html")
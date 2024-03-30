from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *


##########################################
# Iniciar sesión
##########################################
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(),
        min_length=4,
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8,
    )

##########################################
# Registro
##########################################
class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(),
        min_length=4,
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(),
        min_length=4,
    )

    password = forms.CharField(
        label="Clave",
        widget=forms.PasswordInput(),
        min_length=8,
    )
    
    password_confirm = forms.CharField(
        label="Confirmar Clave",
        widget=forms.PasswordInput(),
        min_length=8,
    )

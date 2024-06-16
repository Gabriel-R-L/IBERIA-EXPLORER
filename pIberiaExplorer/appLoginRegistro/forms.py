from django import forms
from django.utils.translation import gettext_lazy as _

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


##########################################
# Login/Register Form
class LoginRegisterForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'Correo electrónico'
        }),
        min_length=4,
    )
        
        
##########################################
# Iniciar sesión
##########################################
class LoginForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'Clave'
        }),
        min_length=8,
    )
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    

##########################################
# Registro
##########################################
class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'Nombre de Usuario'
        }),
        min_length=4,
    )

    password = forms.CharField(
        label="Clave",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'Clave'
        }),
        min_length=8,
    )
    
    password_confirm = forms.CharField(
        label="Confirmar Clave",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'Confirmar Clave'
        }),
        min_length=8,
    )
   
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

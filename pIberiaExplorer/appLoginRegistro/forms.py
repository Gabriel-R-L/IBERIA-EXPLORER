from django import forms
from django.utils.translation import gettext_lazy as _

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


##########################################
# Login/Register Form
class LoginRegisterForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(),
        min_length=4,
    )
        
        
##########################################
# Iniciar sesión
##########################################
class LoginForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8,
    )
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    

##########################################
# Registro
##########################################
class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(),
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
   
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

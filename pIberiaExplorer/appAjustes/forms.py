from os import read
from random import choice
from django import forms
from django.utils.translation import gettext_lazy as _

from appLoginRegistro.models import Usuario
from appAjustes.models import UsuarioPreferencia
from appIberiaExplorer.models import AtributoPlan


############################################
# Formulario de configuracion de la cuenta
class ConfiguracionCuentaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('username', 'apellido_1', 'apellido_2', 'foto_perfil', 'email', 'telefono', 'direccion', 'id_ciudad')
        
        labels = {
            'username': _('Nombre de usuario'),
            'apellido_1': _('Primer apellido'),
            'apellido_2': _('Segundo apellido'),
            'foto_perfil': _('Foto de perfil'),
            'email': _('Correo electrónico'),
            'telefono': _('Teléfono'),
            'direccion': _('Dirección'),
            'id_ciudad': _('Ciudad'),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
        self.fields['apellido_1'].widget.attrs.update({
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
        self.fields['apellido_2'].widget.attrs.update({
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
        self.fields['foto_perfil'].widget.attrs.update({
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 bg-gray-200',
            'readonly': 'readonly'
        })
        self.fields['telefono'].widget.attrs.update({
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
        self.fields['direccion'].widget.attrs.update({
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
        self.fields['id_ciudad'].widget.attrs.update({
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })


############################################
# Cambiar contraseña
class CambiarContraseñaForm(forms.Form):
    contrasena_actual = forms.CharField(
        label=_('Contraseña actual'), 
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
    )
    contrasena_nueva = forms.CharField(
        label=_('Contraseña nueva'), 
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
    )
    contrasena_nueva_repetida = forms.CharField(
        label=_('Repetir contraseña nueva'), 
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        contrasena_nueva = cleaned_data.get('contrasena_nueva')
        contrasena_nueva_repetida = cleaned_data.get('contrasena_nueva_repetida')
        if contrasena_nueva and contrasena_nueva_repetida and contrasena_nueva != contrasena_nueva_repetida:
            self.add_error('contrasena_nueva_repetida', _('Las contraseñas no coinciden.'))
        return cleaned_data
    
############################################
# AñadirPreferencia
class AñadirPreferencia(forms.Form):
    atributo_plan = forms.ChoiceField(
        label=_('Atributos disponibles'),
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
    )
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        choices = []
        seen = set() # Para evitar duplicados
        
        for ap in AtributoPlan.objects.all():
            if ap.nombre not in seen and not UsuarioPreferencia.objects.filter(usuario=usuario, atributo_plan__nombre=ap.nombre):
                seen.add(ap.nombre)
                choices.append((ap.id_atributo_plan, ap.nombre))
            
        if not choices:
            choices.append((None, _('No hay atributos disponibles')))
                
        self.fields['atributo_plan'].choices = choices
    
############################################
# Cambiar foto perfil
############################################
class CambiarFotoPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto_perfil']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
from django import forms
from django.utils.translation import gettext_lazy as _

from appLoginRegistro.models import Usuario


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


############################################
# Cambiar contraseña
class CambiarContrasenaForm(forms.Form):
    contrasena_actual = forms.CharField(label=_('Contraseña actual'), widget=forms.PasswordInput)
    contrasena_nueva = forms.CharField(label=_('Contraseña nueva'), widget=forms.PasswordInput)
    contrasena_nueva_repetida = forms.CharField(label=_('Repetir contraseña nueva'), widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        contrasena_nueva = cleaned_data.get('contrasena_nueva')
        contrasena_nueva_repetida = cleaned_data.get('contrasena_nueva_repetida')
        if contrasena_nueva and contrasena_nueva_repetida and contrasena_nueva != contrasena_nueva_repetida:
            self.add_error('contrasena_nueva_repetida', _('Las contraseñas no coinciden.'))
        return cleaned_data
    

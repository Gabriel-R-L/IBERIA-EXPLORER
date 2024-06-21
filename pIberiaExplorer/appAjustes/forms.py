from django import forms

from appLoginRegistro.models import Usuario
from appAjustes.models import UsuarioPreferencia
from appIberiaExplorer.models import AtributoPlan


############################################
# CONFIGURACIÓN DE CUENTA
############################################
class ConfiguracionCuentaForm(forms.ModelForm):
    form_id = forms.CharField(widget=forms.HiddenInput(), initial='configuracion_cuenta_form')
    class Meta:
        model = Usuario
        fields = ['username', 'apellido_1', 'apellido_2', 'foto_perfil', 'email', 'telefono', 'direccion', 'id_ciudad']
        
        labels = {
            'username': 'Nombre de usuario',
            'apellido_1': 'Primer apellido',
            'apellido_2': 'Segundo apellido',
            'foto_perfil': '',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'id_ciudad': 'Ciudad',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
            }),
            'apellido_1': forms.TextInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
            }),
            'apellido_2': forms.TextInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'style': 'display: none; position: absolute; right: 0; bottom: 0; opacity: 0; overflow: hidden; width: 0; height: 0;'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 bg-gray-200',
                'readonly': 'readonly'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
            }),
            'id_ciudad': forms.Select(attrs={
                'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'readonly': 'readonly'
        })


############################################
# CAMBIAR CONTRASEÑA
############################################
class CambiarContraseñaForm(forms.Form):
    form_id = forms.CharField(widget=forms.HiddenInput(), initial='cambiar_contraseña_form')
    contraseña_actual = forms.CharField(
        label='Contraseña actual', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        }),
        min_length=8,
    )
    contraseña_nueva = forms.CharField(
        label='Contraseña nueva', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        }),
        min_length=8,
    )
    contraseña_nueva_repetida = forms.CharField(
        label='Repetir contraseña nueva', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        }),
        min_length=8,
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
############################################
# AÑADIR PREFERENCIA
############################################
class AñadirPreferencia(forms.Form):
    atributo_plan = forms.ChoiceField(
        label='Atributos disponibles',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 dark:color-gray-300'
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
            choices.append((None, 'No hay atributos disponibles'))
                
        self.fields['atributo_plan'].choices = choices
    
from django import forms
from django.utils.translation import gettext_lazy as _
from appIberiaExplorer.models import AtributoPlan

############################################
# MostrarPreferencia
class BuscadorPreferenciaFecha(forms.Form):
    atributo_plan = forms.ChoiceField(
        label=_('Atributos disponibles'),
        required=False,
        initial=None,
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'})
    )
    
    fecha_inicio = forms.DateField(
        label=_('Fecha de inicio'),
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'dd/mm/aaaa',
            'type': 'date'
        })
    )
    
    fecha_fin = forms.DateField(
        label=_('Fecha de fin'),
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'dd/mm/aaaa',
            'type': 'date'
        })
    )
    
    def __init__(self, *args, **kwargs):
        selected_atributo_plan = kwargs.pop('selected_atributo_plan', None)
        super().__init__(*args, **kwargs)
        
        choices = [('', _('-- Seleccione un atributo --'))]
        seen = set()  # Para evitar duplicados
        
        for ap in AtributoPlan.objects.all():
            if ap.nombre not in seen:
                seen.add(ap.nombre)
                choices.append((ap.id_atributo_plan, ap.nombre))
            
        if not choices:
            choices.append((None, _('No hay atributos disponibles')))
        
        if selected_atributo_plan:
            try:
                nombre_atributo = AtributoPlan.objects.get(id_atributo_plan=selected_atributo_plan).nombre.replace("/", "")
                choices = [(selected_atributo_plan, nombre_atributo)] + [
                    choice for choice in choices if choice[0] != selected_atributo_plan
                ]
            except AtributoPlan.DoesNotExist:
                pass  # Manejo de excepción si el atributo seleccionado no existe
                
        self.fields['atributo_plan'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                self.add_error('fecha_inicio', _('La fecha de inicio no puede ser mayor que la fecha de fin'))
        
        return cleaned_data
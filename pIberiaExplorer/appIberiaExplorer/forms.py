from django import forms
from django.utils.translation import gettext_lazy as _
from appIberiaExplorer.models import AtributoPlan


############################################
# MostrarPreferencia
class MostrarPreferencia(forms.Form):
    atributo_plan = forms.ChoiceField(
        label=_('Atributos disponibles')
    )
    
    def __init__(self, *args, **kwargs):
        selected_atributo_plan = kwargs.pop('selected_atributo_plan', None)
        super().__init__(*args, **kwargs)
        choices = []
        seen = set() # Para evitar duplicados
        
        for ap in AtributoPlan.objects.all():
            if ap.nombre not in seen:
                seen.add(ap.nombre)
                choices.append((ap.id_atributo_plan, ap.nombre))
            
        if not choices:
            choices.append((None, _('No hay atributos disponibles')))
                
        if selected_atributo_plan:
            nombre_atributo = AtributoPlan.objects.get(id_atributo_plan=selected_atributo_plan).nombre.replace("/", "")
            choices = [(nombre_atributo, dict(choices).get(nombre_atributo))] + [
                choice for choice in choices if choice[0] != nombre_atributo
            ]

        self.fields['atributo_plan'].choices = choices
        
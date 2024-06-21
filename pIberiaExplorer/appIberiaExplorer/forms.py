from django import forms
from appIberiaExplorer.models import AtributoPlan


############################################
# MOSTRARPREFERENCIA
############################################
from django import forms
from appIberiaExplorer.models import AtributoPlan

class BuscadorPreferenciaFecha(forms.Form):
    # Campo de selección para atributos del plan
    atributo_plan = forms.ChoiceField(
        label='Atributos disponibles',  # Etiqueta del campo
        required=False,  # Campo no obligatorio
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })  # Apariencia del campo en el formulario
    )
    
    # Campo de fecha para la fecha de inicio
    fecha_inicio = forms.DateField(
        label='Fecha de inicio',  # Etiqueta del campo
        required=False,  # Campo no obligatorio
        widget=forms.DateInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'dd/mm/aaaa',  # Texto de marcador de posición
            'type': 'date'  # Tipo de entrada como fecha
        })
    )
    
    # Campo de fecha para la fecha de fin
    fecha_fin = forms.DateField(
        label='Fecha de fin',  # Etiqueta del campo
        required=False,  # Campo no obligatorio
        widget=forms.DateInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'dd/mm/aaaa',  # Texto de marcador de posición
            'type': 'date'  # Tipo de entrada como fecha
        })
    )
    
    def __init__(self, *args, **kwargs):
        # Obtiene el atributo del plan seleccionado de los argumentos
        selected_atributo_plan = kwargs.pop('selected_atributo_plan', None)
        super().__init__(*args, **kwargs)
        
        # Inicializa las opciones del campo de selección de atributo
        choices = [('', '-- Seleccione un atributo --')]  # Opción predeterminada
        seen = set()  # Conjunto para evitar duplicados
        
        # Itera sobre todos los atributos del plan y agrega opciones únicas
        for ap in AtributoPlan.objects.all():
            if ap.nombre not in seen:
                seen.add(ap.nombre)
                choices.append((ap.id_atributo_plan, ap.nombre))
            
        # Si no hay opciones disponibles, agrega una opción indicativa
        if not choices:
            choices.append((None, 'No hay atributos disponibles'))
        
        # Maneja la selección del atributo del plan si existe
        if selected_atributo_plan:
            try:
                nombre_atributo = AtributoPlan.objects.get(id_atributo_plan=selected_atributo_plan).nombre
                # Elimina la opción seleccionada de las opciones disponibles
                choices = [
                    choice for choice in choices if choice != (selected_atributo_plan, nombre_atributo)
                ]
            except AtributoPlan.DoesNotExist:
                pass  # Manejo de excepción si el atributo seleccionado no existe
                
        # Asigna las opciones finales al campo de selección de atributo
        self.fields['atributo_plan'].choices = choices

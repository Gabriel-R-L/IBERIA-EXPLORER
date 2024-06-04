from django.shortcuts import render
import os

##########################################
# Borrar foto perfil
def borrar_foto_perfil(foto_perfil):
    from django.conf import settings
    # No borrar la foto por defecto para otros usuarios
    if foto_perfil and 'default.png' not in foto_perfil: 
            p = f'/img/profile_pictures/{foto_perfil}'
            avatar_path = os.path.join(settings.MEDIA_ROOT, p)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
            
##########################################
# Configuracion de la cuenta
def configuracion_cuenta(request):
    from appLoginRegistro.models import Usuario
    from .forms import ConfiguracionCuentaForm, CambiarContrasenaForm
    from django.utils.translation import gettext_lazy as _
    
    usuario = request.user
    if request.method == 'POST':
        form = ConfiguracionCuentaForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario.username = form.cleaned_data['username']
            usuario.first_name = form.cleaned_data['first_name']
            usuario.last_name = form.cleaned_data['last_name']
            usuario.email = form.cleaned_data['email']
            if form.cleaned_data['foto_perfil']:
                borrar_foto_perfil(usuario.foto_perfil)
                usuario.foto_perfil = form.cleaned_data['foto_perfil']
            usuario.save()
            return render(request, 'appAjustes/configuracion_cuenta.html', {'form': form, 'mensaje': _('Cambios guardados correctamente.')})
    else:
        form_datos = ConfiguracionCuentaForm(instance=usuario)
        form_cambio_pssw = CambiarContrasenaForm()
        
        context = {
            'form_datos': form_datos,
            'form_cambio_pssw': form_cambio_pssw,
        }
        
    return render(request, 'appAjustes/configuracion_cuenta.html', context=context)
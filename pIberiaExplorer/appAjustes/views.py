from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import os

from .forms import *
from appLoginRegistro.models import Usuario
from appIberiaExplorer.models import AtributoPlan
from appAjustes.models import UsuarioPreferencia

from pIberiaExplorer.utils import APP_AJUSTES


##########################################
# BORRAR FOTO DE PERFIL
##########################################
def borrar_foto_perfil(id_usuario, foto_perfil):
    from django.conf import settings
    # No borrar la foto por defecto para otros usuarios
    if foto_perfil and 'default.png' not in foto_perfil: 
            p = f'/img/profile_pictures/{foto_perfil}'
            avatar_path = os.path.join(settings.MEDIA_ROOT, p)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            usuario.foto_perfil = os.path.join(settings.MEDIA_ROOT, '/img/profile_pictures/default.png')
            usuario.save()
            
            
##########################################
# CONFIGURACION DE CUENTA
##########################################
def configuracion_cuenta(request):
    from appLoginRegistro.models import Usuario
    from .forms import ConfiguracionCuentaForm, CambiarContrasenaForm
    from django.utils.translation import gettext_lazy as _
    
    usuario = Usuario.objects.get(id_usuario=request.user.id_usuario)
    context = { }
    
    if request.method == 'POST':
        form = ConfiguracionCuentaForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario.username = form.cleaned_data['username']
            usuario.first_name = form.cleaned_data['first_name']
            usuario.last_name = form.cleaned_data['last_name']
            usuario.email = form.cleaned_data['email']
            if form.cleaned_data['foto_perfil']:
                borrar_foto_perfil(usuario.id_usuario, usuario.foto_perfil)
                usuario.foto_perfil = form.cleaned_data['foto_perfil']
            usuario.save()
            
            form_cambio_pssw = CambiarContrasenaForm()
            
            context = {
                'mensaje_error': _('Cambios guardados correctamente.'),
                'form_datos': form,
                'form_cambio_pssw': CambiarContrasenaForm()
            }
    else:
        form_datos = ConfiguracionCuentaForm(instance=usuario)
        form_cambio_pssw = CambiarContrasenaForm()
        
        context = {
            'form_datos': form_datos,
            'form_cambio_pssw': form_cambio_pssw,
        }
        
    return render(request, f'{APP_AJUSTES}/configuracion_cuenta.html', context=context)


##########################################
# VER DATOS
##########################################
def ver_datos(request):
    from appCarritoPedido.models import Pedido, PedidoDetalle
    from django.utils.translation import gettext_lazy as _
    
    usuario = request.user
    
    pedidos = Pedido.objects.filter(id_cliente=usuario)
    nombre_plan = PedidoDetalle.objects.filter(id_pedido__in=pedidos).values('id_plan__titulo').distinct()
    preferencias = UsuarioPreferencia.objects.filter(usuario=usuario)
    
    context = {
        'usuario': usuario,
        'pedidos': pedidos,
        'nombre_plan': nombre_plan,
        'preferencias': preferencias,
    }
    
    return render(request, f'{APP_AJUSTES}/ver_datos.html', context=context)


##########################################
# BORRAR PREFERENCIA
##########################################
@login_required(login_url='/registro/')
def borrar_preferencia(request, id_preferencia):
    preferencia = get_object_or_404(UsuarioPreferencia, id_preferencia=id_preferencia)
    preferencia.delete()
    
    return redirect('/ajustes/mis-datos')


##########################################
# AÑADIR PREFERENCIA
##########################################
@login_required(login_url='/registro/')
def añadir_preferencia(request):
    from appAjustes.models import UsuarioPreferencia
    usuario = request.user
    
    if request.method == 'POST':
        form = AñadirPreferencia(request.POST, usuario=usuario)
        if form.is_valid():
            atributo_plan_id = form.cleaned_data['atributo_plan']
            atributo_plan = AtributoPlan.objects.get(id_atributo_plan=atributo_plan_id)

            preferencia, created = UsuarioPreferencia.objects.get_or_create(atributo_plan=atributo_plan, usuario=usuario)
            
            if not created:
                preferencia.save()
            
                context = {
                    'mensaje_error': 'Preferencia añadida correctamente.'
                }
                
                return redirect('/ajustes/mis-datos', context=context)
                
            return redirect('/ajustes/mis-datos')
    else:
        form = AñadirPreferencia(usuario=request.user)
        context = {
            'form': form
        }
        return render(request, f'{APP_AJUSTES}/añadir_preferencia.html', context=context)
    
    
##########################################
# CAMBIAR FOTO DE PERFIL
##########################################
@login_required(login_url='/registro/')
def cambiar_foto_perfil(request):
    from appLoginRegistro.models import Usuario
    from .forms import CambiarFotoPerfilForm
    from django.utils.translation import gettext_lazy as _
    
    usuario = request.user
    
    if request.method == 'POST':
        form = CambiarFotoPerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            borrar_foto_perfil(usuario.id_usuario, usuario.foto_perfil)
            Usuario.objects.filter(id_usuario=usuario.id_usuario).update(foto_perfil=form.cleaned_data['foto_perfil'])
            
            redirect('/ajustes/configuracion-cuenta', context={'mensaje_error': 'Foto de perfil cambiada correctamente.'})
    else:
        form = CambiarFotoPerfilForm(instance=usuario)
        context = {
            'form': form
        }
        
    return redirect('/ajustes/configuracion-cuenta', context=context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import os

from .forms import *
from appLoginRegistro.models import Usuario
from appIberiaExplorer.models import AtributoPlan
from appAjustes.models import UsuarioPreferencia

from pIberiaExplorer.utils import APP_AJUSTES


##########################################
# CONFIGURACION DE CUENTA
##########################################
def configuracion_cuenta(request):
    # Obtiene el usuario actual
    usuario = Usuario.objects.get(id_usuario=request.user.id_usuario)
    
    if request.method == 'POST':
        # Maneja el formulario de configuración de cuenta
        if request.POST.get('form_id') == 'configuracion_cuenta_form':
            form_datos = ConfiguracionCuentaForm(request.POST, request.FILES, instance=usuario)
            form_cambio_pssw = CambiarContraseñaForm(request.POST)
            
            if 'foto_perfil' in request.FILES:
                print(usuario.foto_perfil)
                borrar_foto_perfil(usuario.id_usuario, usuario.foto_perfil)
            
            if form_datos.is_valid():
                # Actualiza los datos del usuario
                usuario.username = form_datos.cleaned_data.get('username', usuario.username)
                usuario.apellido_1 = form_datos.cleaned_data.get('apellido_1', usuario.apellido_1)
                usuario.apellido_2 = form_datos.cleaned_data.get('apellido_2', usuario.apellido_2)
                usuario.email = form_datos.cleaned_data.get('email', usuario.email)
                usuario.telefono = form_datos.cleaned_data.get('telefono', usuario.telefono)
                usuario.direccion = form_datos.cleaned_data.get('direccion', usuario.direccion)
                usuario.id_ciudad = form_datos.cleaned_data.get('id_ciudad', usuario.id_ciudad)
                
                # Maneja la actualización de la foto de perfil
                if 'foto_perfil' in request.FILES:
                    usuario.foto_perfil = request.FILES['foto_perfil']
                usuario.save()
                
                # Redirige con mensaje de éxito
                context = {
                    'mensaje_error': 'Cambios guardados correctamente.',
                    'form_datos': form_datos,
                    'form_cambio_pssw': form_cambio_pssw
                }
                return redirect('/ajustes/configuracion-cuenta', context=context)
            else:
                # Muestra mensaje de error si el formulario no es válido
                context = {
                    'mensaje_error': 'Error al guardar los cambios.',
                    'form_datos': form_datos,
                    'form_cambio_pssw': form_cambio_pssw
                }
                return render(request, f'{APP_AJUSTES}/configuracion_cuenta.html', context=context) 
            
        # Maneja el formulario de cambio de contraseña
        elif request.POST.get('form_id') == 'cambiar_contraseña_form':
            form_datos = ConfiguracionCuentaForm(instance=usuario)
            form_cambio_pssw = CambiarContraseñaForm(request.POST)
            if form_cambio_pssw.is_valid():
                # Verifica la contraseña actual
                if usuario.check_password(form_cambio_pssw.cleaned_data['contraseña_actual']):
                    # Verifica que las nuevas contraseñas coincidan
                    if form_cambio_pssw.cleaned_data['contraseña_nueva'] != form_cambio_pssw.cleaned_data['contraseña_nueva_repetida']:
                        context = {
                            'mensaje_error': 'Las contraseñas no coinciden.',
                            'sub_mensaje_error': 'La nueva contraseña y su repetición no coinciden.',
                            'form_datos': form_datos,
                            'form_cambio_pssw': form_cambio_pssw
                        }
                        return render(request, f'{APP_AJUSTES}/configuracion_cuenta.html', context=context)
                    
                    # Verifica que la nueva contraseña no sea igual a la actual
                    if form_cambio_pssw.cleaned_data['contraseña_actual'] == form_cambio_pssw.cleaned_data['contraseña_nueva']:
                        context = {
                            'mensaje_error': 'Las contraseñas no pueden ser iguales.',
                            'sub_mensaje_error': 'La nueva contraseña no puede ser igual a la actual.',
                            'form_datos': form_datos,
                            'form_cambio_pssw': form_cambio_pssw
                        }
                        return render(request, f'{APP_AJUSTES}/configuracion_cuenta.html', context=context)
                    
                    # Establece la nueva contraseña
                    usuario.set_password(form_cambio_pssw.cleaned_data['contraseña_nueva'])
                    usuario.save()
                    
                    # Redirige al registro
                    return redirect('/registro')
                else:
                    # Muestra error si la contraseña actual es incorrecta
                    context = {
                        'mensaje_error': 'Error al guardar los cambios.',
                        'sub_mensaje_error': 'La contraseña actual no es correcta.',
                        'form_datos': form_datos,
                        'form_cambio_pssw': form_cambio_pssw
                    }
                    return render(request, f'{APP_AJUSTES}/configuracion_cuenta.html', context=context)
            else:
                # Muestra error si el formulario no es válido
                context = {
                    'mensaje_error': 'Error al guardar los cambios.',
                    'form_datos': form_datos,
                    'form_cambio_pssw': form_cambio_pssw
                }
                return render(request, f'{APP_AJUSTES}/configuracion_cuenta.html', context=context)
    else:
        # Si no es POST, muestra los formularios vacíos
        form_datos = ConfiguracionCuentaForm(instance=usuario)
        form_cambio_pssw = CambiarContraseñaForm()
        
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
    
    usuario = request.user
    
    # Obtiene todos los pedidos del usuario actual
    pedidos = Pedido.objects.filter(id_cliente=usuario)
    for pedido in pedidos:
        # Asigna el nombre del plan a cada pedido
        pedido.nombre_plan = PedidoDetalle.objects.filter(id_pedido=pedido).first().id_plan.titulo
    
    # Obtiene todas las preferencias del usuario
    preferencias = UsuarioPreferencia.objects.filter(usuario=usuario)
    
    context = {
        'usuario': usuario,
        'pedidos': pedidos,
        'preferencias': preferencias,
    }
    
    return render(request, f'{APP_AJUSTES}/ver_datos.html', context=context)


##########################################
# FOTO DE PERFIL
##########################################
def borrar_foto_perfil(id_usuario, foto_perfil):
    from django.conf import settings
    if foto_perfil and 'default.png' not in foto_perfil: 
        avatar_path = os.path.join(settings.MEDIA_ROOT, str(foto_perfil))
        try:
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
                print(f"Archivo {avatar_path} eliminado con éxito.")
            else:
                print(f"El archivo {avatar_path} no existe.")
        except PermissionError as e:
            print(f"No se pudo eliminar el archivo {avatar_path}: {e}")
        except Exception as e:
            print(f"Ocurrió un error al intentar eliminar el archivo {avatar_path}: {e}")


##########################################
# PREFERENCIAS
##########################################
@login_required(login_url='/registro/')
def añadir_preferencia(request):
    usuario = request.user
    
    if request.method == 'POST':
        form = AñadirPreferencia(request.POST, usuario=usuario)
        if form.is_valid():
            # Añade la nueva preferencia
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
    
@login_required(login_url='/registro/')
def borrar_preferencia(request, id_preferencia):
    # Borra la preferencia especificada
    preferencia = get_object_or_404(UsuarioPreferencia, id_preferencia=id_preferencia)
    preferencia.delete()
    
    return redirect('/ajustes/mis-datos')

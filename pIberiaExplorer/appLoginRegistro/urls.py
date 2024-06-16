from django.urls import path
from .views import *

from pIberiaExplorer.utils import APP_LOGIN_REGISTRO
app_name = APP_LOGIN_REGISTRO

urlpatterns = [
    path("", login_register, name="login_register"),   
    path("login/", login, name="login"),   
    path("register/", register, name="register"),
    
    # Logout
    path("logout/", logout, name="logout"),
    path("logout-confirmation/", logout_confirmation, name="logout_confirmation"),
    
    # Borrar cuenta
    path("delete_account/", delete_account, name="delete_account"),
    path("delete_account_confirmation/", delete_account_confirmation, name="delete_account_confirmation"),
    
    # Confirmar correo
    path("confirm_email/<str:token>/", confirm_email, name="confirm_email"),
    path("email_confirmed/", email_confirmed, name="email_confirmed"),
    
    # Recuperar contraseña
    path("recuperar_contraseña/", recuperar_contraseña, name="recuperar_contraseña"), 
    path("cambiar_contraseña/<str:token>/", recover_pssw, name="recover_pssw")
]

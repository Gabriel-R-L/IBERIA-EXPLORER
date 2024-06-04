from django.urls import path, include
from requests import delete
from .views import delete_account, delete_account_confirmation, login_register, login, logout_confirmation, register, logout, confirm_email, email_confirmed

app_name = "appLoginRegistro"

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
]

from django.urls import path, include
from .views import login_register, login, register, logout, confirm_email, email_confirmed

app_name = "appLoginRegistro"

urlpatterns = [
    path("", login_register, name="login_register"),   
    path("login/", login, name="login"),   
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    
    # Confirmar correo
    path("confirm_email/<str:token>/", confirm_email, name="confirm_email"),
    path("email_confirmed/", email_confirmed, name="email_confirmed"),
]

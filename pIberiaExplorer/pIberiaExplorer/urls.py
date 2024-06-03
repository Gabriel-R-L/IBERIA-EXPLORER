"""
URL configuration for pIberiaExplorer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from appLoginRegistro.views import google_login_redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('accounts/signup/', google_login_redirect, name='account_signup'),
    # APPS
    path("", include("appIberiaExplorer.urls", namespace="appIberiaExplorer")),
    path("registro/", include("appLoginRegistro.urls", namespace="appLoginRegistro")),
    path("carrito/", include("appCarritoPedido.urls", namespace="appCarritoPedido")),
    path("notificaciones/", include("appNotificaciones.urls", namespace="appNotificaciones")),
]


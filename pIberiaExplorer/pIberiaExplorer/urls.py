from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("g/", include("allauth.urls")), # Para la funcionalidad de autenticación de Google (no es necesario para el proyecto)
    
    # APPS
    path("", include("appIberiaExplorer.urls", namespace="appIberiaExplorer")),
    path("registro/", include("appLoginRegistro.urls", namespace="appLoginRegistro")),
    path("carrito/", include("appCarritoPedido.urls", namespace="appCarritoPedido")),
    path("notificaciones/", include("appNotificaciones.urls", namespace="appNotificaciones")),
    path("ajustes/", include("appAjustes.urls", namespace="appAjustes")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Para servir archivos multimedia en desarrollo


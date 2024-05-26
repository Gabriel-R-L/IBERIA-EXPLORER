from django.apps import AppConfig


class ApploginregistroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appLoginRegistro'
    
    def ready(self):
        import appLoginRegistro.signals
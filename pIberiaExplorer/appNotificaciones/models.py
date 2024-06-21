from django.utils import timezone
from django.db import models
from appLoginRegistro.models import Usuario


##################################################
# NOTIFICACIONES
##################################################
class Notificacion(models.Model):   
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.PROTECT)
    titulo_notificacion = models.CharField("Titulo",null=True, blank=True)
    mensaje_notificacion = models.TextField("Mensaje",blank=True, null=True)	
    timestamp = models.DateTimeField("Fecha del Sistema",default=timezone.now)
    leido = models.BooleanField("Leído", default=False)
    
    class Meta:
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"
        ordering = ['-timestamp']
		
    def __str__(self):
         return f"{self.id},{self.usuario},{self.titulo_notificacion},{self.mensaje_notificacion},{self.timestamp}"

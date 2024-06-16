from django.db import models


####################################################
# USUARIOPREFERENCIA
####################################################
class UsuarioPreferencia(models.Model):
    from appLoginRegistro.models import Usuario
    from appIberiaExplorer.models import AtributoPlan
    
    id_preferencia = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    atributo_plan = models.ForeignKey(
        AtributoPlan, on_delete=models.CASCADE, null=True
    )

    class Meta:
        managed = True
        verbose_name = "UsuarioPreferencia"
        verbose_name_plural = "UsuarioPreferencias"
        
    def __str__(self):
        return f"{self.usuario.username}, {self.atributo_plan.nombre}"

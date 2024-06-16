from django.db import models


####################################################
# CONTINENTE
####################################################
class Continente(models.Model):
    id_continente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = True
        verbose_name = "Continente"
        verbose_name_plural = "Continentes"
        
    def __str__(self):
        return self.nombre


####################################################
# PAIS
####################################################
class Pais(models.Model):
    id_pais = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    continente = models.ForeignKey(Continente, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Pais"
        verbose_name_plural = "Paises"
        
    def __str__(self):
        return f"{self.nombre}, {self.continente}"


####################################################
# CIUDAD
####################################################
class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
    
    def __str__(self):
        return f"{self.nombre}"


####################################################
# PLAN
####################################################
class Plan(models.Model):
    id_plan = models.AutoField(primary_key=True)
    id_plan_api = models.IntegerField(null=True, default=0)
    titulo = models.CharField(max_length=255)
    precio = models.FloatField()
    descripcion = models.CharField(max_length=255)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)
    hora_inicio = models.TimeField(null=True)
    nombre_lugar = models.CharField(max_length=255, null=True)
    codigo_postal = models.CharField(max_length=5, null=True)
    nombre_calle = models.CharField(max_length=255, null=True)
    organizador = models.CharField(max_length=255, null=True)

    class Meta:
        managed = True
        verbose_name = "Plan"
        verbose_name_plural = "Planes"
        
    def __str__(self):
        return f"{self.titulo}, {self.precio}, {self.id_plan_api}"
        

####################################################
# ATRIBUTOPLAN
####################################################
class AtributoPlan(models.Model):
    id_atributo_plan = models.AutoField(primary_key=True)
    url = models.CharField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        verbose_name = "AtributoPlan"
        verbose_name_plural = "AtributoPlanes"
        
    def __str__(self):
        return f"{self.nombre}, {self.url}, {self.plan}"
    
    def save(self, *args, **kwargs):
        import re
        if self.url:
            self.nombre = re.sub(r'(?<=[a-z])(?=[A-Z])', '/', self.url.split('/')[-1])
        super().save(*args, **kwargs)


        
        
######################################################################################################################################
######################################################################################################################################

""" 
# 5 Proveedor
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=12)
    email = models.EmailField()
    id_ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores" """


# 6 TipoPlan
""" class TipoPlan(models.Model):
    TIPO_PLAN = [
        ("Api", 1),
        ("Manual", 2),
        ("Otro", 3)
    ]
    id_tipo_plan = models.AutoField(primary_key=True)
    nombre_tipo_plan = models.CharField(max_length=255, choices=TIPO_PLAN, default="Api")
    # id_atributo_plan = models.ForeignKey(AtributoPlan, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "TipoPlan"
        verbose_name_plural = "TipoPlanes" """


# 10 Favorito
# class Favorito(models.Model):
#     from appLoginRegistro.models import Usuario
#     id_favorito = models.AutoField(primary_key=True)
#     id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
#     id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)

#     class Meta:
#         managed = True
#         verbose_name = "Favorito"
#         verbose_name_plural = "Favoritos"


# 11 Comentario
""" class Comentario(models.Model):
    from appLoginRegistro.models import Usuario
    id_comentario = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=255)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios" """


# 13 EstadoReserva
# class EstadoReserva(models.Model):
#     id_estado_reserva = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=255)
#     detalles = models.CharField(max_length=255)
#     id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

#     class Meta:
#         managed = True
#         verbose_name = "EstadoReserva"
#         verbose_name_plural = "EstadoReservas"


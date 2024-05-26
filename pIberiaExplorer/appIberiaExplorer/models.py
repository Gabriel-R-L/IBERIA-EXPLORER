from django.db import models


# 1 Continente
class Continente(models.Model):
    id_continente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = True
        verbose_name = "Continente"
        verbose_name_plural = "Continentes"


# 2 Pais
class Pais(models.Model):
    id_pais = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    id_continente = models.ForeignKey(Continente, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Pais"
        verbose_name_plural = "Paises"


# 3 Ciudad
class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    id_continente = models.ForeignKey(Continente, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"


# 4 AtributoPlan
class AtributoPlan(models.Model):
    id_atributo_plan = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    precio = models.FloatField()
    duracion = models.IntegerField()
    admite_perro = models.IntegerField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    class Meta:
        managed = True
        verbose_name = "AtributoPlan"
        verbose_name_plural = "AtributoPlanes"


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
        verbose_name_plural = "Proveedores"


# 6 TipoPlan
class TipoPlan(models.Model):
    id_tipo_plan = models.AutoField(primary_key=True)
    nombre_tipo_plan = models.CharField(max_length=255)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    id_atributo_plan = models.ForeignKey(AtributoPlan, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "TipoPlan"
        verbose_name_plural = "TipoPlanes"


# 7 Plan
class Plan(models.Model):
    id_plan = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    precio = models.FloatField()
    duracion = models.IntegerField()
    fecha_inicio = models.DateTimeField()
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    id_tipo_plan = models.ForeignKey(TipoPlan, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Plan"
        verbose_name_plural = "Planes"


# 8 UsuarioPreferencias
class UsuarioPreferencia(models.Model):
    from appLoginRegistro.models import Usuario
    id_preferencia = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    id_atributo_plan_plan = models.ForeignKey(
        AtributoPlan, on_delete=models.CASCADE, null=True
    )

    class Meta:
        managed = True
        verbose_name = "UsuarioPreferencia"
        verbose_name_plural = "UsuarioPreferencias"


# 10 Favorito
class Favorito(models.Model):
    from appLoginRegistro.models import Usuario
    id_favorito = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"


# 11 Comentario
class Comentario(models.Model):
    from appLoginRegistro.models import Usuario
    id_comentario = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=255)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"


# 12 Notificacion
class Notificacion(models.Model):
    from appLoginRegistro.models import Usuario
    id_notificacion = models.AutoField(primary_key=True)
    texto_notificacion = models.CharField(max_length=255)
    hora_notificacion = models.DateTimeField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"


# 13 EstadoReserva
class EstadoReserva(models.Model):
    id_estado_reserva = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    detalles = models.CharField(max_length=255)
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "EstadoReserva"
        verbose_name_plural = "EstadoReservas"


# 14 Reserva
class Reserva(models.Model):
    from appLoginRegistro.models import Usuario
    id_reserva = models.AutoField(primary_key=True)
    fecha_reserva = models.DateTimeField()
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    id_estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.CASCADE)
    id_tipo_plan = models.ForeignKey(TipoPlan, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

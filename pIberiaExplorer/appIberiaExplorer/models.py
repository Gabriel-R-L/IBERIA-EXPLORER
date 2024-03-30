from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from django.utils import timezone


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


# 9 Usuario
class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Introduce un email válido")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self, username=None, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(username, email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    #! PARA DEBUG UNIQUE=TRUE, PERO DEBE SER FALSE
    username = models.CharField(max_length=255, null=True, unique=True)
    apellido_1 = models.CharField(max_length=255)
    apellido_2 = models.CharField(max_length=255, null=True)
    #! PARA DEBUG UNIQUE=FALSE, PERO DEBE SER TRUE
    email = models.EmailField(blank=False, null=True, default="", unique=False)
    password = models.CharField(max_length=255)
    telefono = models.CharField(max_length=12, null=True)
    direccion = models.CharField(max_length=75, null=True)
    # activo = models.BooleanField(default=True)
    fecha_baja = models.DateTimeField(null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    email_confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(blank=True, null=True)

    id_ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True)
    id_plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]

    class Meta:
        managed = True
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username or self.email.split("@")[0]


# 8 UsuarioPreferencias
class UsuarioPreferencia(models.Model):
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
    id_favorito = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"


# 11 Comentario
class Comentario(models.Model):
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

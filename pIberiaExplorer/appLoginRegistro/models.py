from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone


############################################
# Usuario
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
    from appIberiaExplorer.models import Ciudad, Plan
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=True)
    apellido_1 = models.CharField(max_length=255, blank=True, null=True)
    apellido_2 = models.CharField(max_length=255, blank=True, null=True)
    foto_perfil = models.ImageField(
          "Foto Perfil"
        , blank=True, null=True
        , upload_to="img/profile_pictures/"
        , default="img/profile_pictures/default.png"
    )
    email = models.EmailField(blank=False, null=False, unique=True)
    password = models.CharField(max_length=255)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.CharField(max_length=75, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    email_confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(blank=True, null=True)

    id_ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        managed = True
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username or self.email.split("@")[0]
    
    def __str__(self):
        return f"{self.id_usuario} - {self.username} -{self.email}"
    

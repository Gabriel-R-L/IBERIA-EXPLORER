# Generated by Django 5.0.6 on 2024-05-22 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AtributoPlan',
            fields=[
                ('id_atributo_plan', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(max_length=255)),
                ('precio', models.FloatField()),
                ('duracion', models.IntegerField()),
                ('admite_perro', models.IntegerField()),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'AtributoPlan',
                'verbose_name_plural': 'AtributoPlanes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id_ciudad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Ciudad',
                'verbose_name_plural': 'Ciudades',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id_comentario', models.AutoField(primary_key=True, serialize=False)),
                ('comentario', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Continente',
            fields=[
                ('id_continente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Continente',
                'verbose_name_plural': 'Continentes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EstadoReserva',
            fields=[
                ('id_estado_reserva', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('detalles', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'EstadoReserva',
                'verbose_name_plural': 'EstadoReservas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id_favorito', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Favorito',
                'verbose_name_plural': 'Favoritos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('texto_notificacion', models.CharField(max_length=255)),
                ('hora_notificacion', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Notificacion',
                'verbose_name_plural': 'Notificaciones',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id_pais', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Pais',
                'verbose_name_plural': 'Paises',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id_plan', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(max_length=255)),
                ('precio', models.FloatField()),
                ('duracion', models.IntegerField()),
                ('fecha_inicio', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Planes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id_reserva', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_reserva', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoPlan',
            fields=[
                ('id_tipo_plan', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo_plan', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'TipoPlan',
                'verbose_name_plural': 'TipoPlanes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UsuarioPreferencia',
            fields=[
                ('id_preferencia', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'UsuarioPreferencia',
                'verbose_name_plural': 'UsuarioPreferencias',
                'managed': True,
            },
        ),
    ]

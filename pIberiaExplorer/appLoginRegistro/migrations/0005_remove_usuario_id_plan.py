# Generated by Django 5.0.6 on 2024-06-04 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appLoginRegistro', '0004_alter_usuario_foto_perfil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='id_plan',
        ),
    ]

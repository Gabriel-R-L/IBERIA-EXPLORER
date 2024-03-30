# Generated by Django 5.0.3 on 2024-03-29 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appIberiaExplorer', '0002_usuario_fecha_baja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.usuario'),
        ),
        migrations.AlterField(
            model_name='favorito',
            name='id_usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.usuario'),
        ),
        migrations.AlterField(
            model_name='notificacion',
            name='id_usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.usuario'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='id_cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.usuario'),
        ),
        migrations.AlterField(
            model_name='usuariopreferencia',
            name='id_usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.usuario'),
        ),
    ]

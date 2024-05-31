# Generated by Django 5.0.6 on 2024-05-28 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCarritoPedido', '0002_carritodetalle_coste_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carritodetalle',
            name='coste_total',
        ),
        migrations.AddField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('COMPLETADO', 'Completado'), ('CANCELADO', 'Cancelado')], default='PENDIENTE', max_length=10),
        ),
    ]
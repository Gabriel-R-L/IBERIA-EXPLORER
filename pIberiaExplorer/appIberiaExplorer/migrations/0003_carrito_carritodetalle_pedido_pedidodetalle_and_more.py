# Generated by Django 5.0.6 on 2024-05-26 14:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appIberiaExplorer', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id_carrito', models.AutoField(primary_key=True, serialize=False)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Carrito',
                'verbose_name_plural': 'Carritos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CarritoDetalle',
            fields=[
                ('id_carrito_detalle', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('id_carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.carrito')),
                ('id_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.plan')),
            ],
            options={
                'verbose_name': 'CarritoDetalle',
                'verbose_name_plural': 'CarritoDetalles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_reserva', models.DateTimeField()),
                ('total', models.FloatField()),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PedidoDetalle',
            fields=[
                ('id_pedido_detalle', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('id_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.pedido')),
                ('id_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.plan')),
            ],
            options={
                'verbose_name': 'PedidoDetalle',
                'verbose_name_plural': 'PedidoDetalles',
                'managed': True,
            },
        ),
        migrations.DeleteModel(
            name='Reserva',
        ),
    ]
# Generated by Django 5.0.6 on 2024-05-27 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appIberiaExplorer', '0004_remove_plan_id_proveedor_remove_plan_id_tipo_plan'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carrito',
            options={'managed': True, 'verbose_name': 'Carrito', 'verbose_name_plural': 'Carrito'},
        ),
    ]

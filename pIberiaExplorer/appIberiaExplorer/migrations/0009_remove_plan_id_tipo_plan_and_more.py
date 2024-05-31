# Generated by Django 5.0.6 on 2024-05-30 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appIberiaExplorer', '0008_remove_tipoplan_id_proveedor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='id_tipo_plan',
        ),
        migrations.RemoveField(
            model_name='tipoplan',
            name='id_atributo_plan',
        ),
        migrations.AlterField(
            model_name='tipoplan',
            name='nombre_tipo_plan',
            field=models.CharField(choices=[('Api', 1), ('Manual', 2), ('Otro', 3)], default='Api', max_length=255),
        ),
    ]

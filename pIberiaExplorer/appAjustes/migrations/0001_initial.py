# Generated by Django 5.0.6 on 2024-06-13 18:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appIberiaExplorer', '0013_remove_comentario_id_plan_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioPreferencia',
            fields=[
                ('id_preferencia', models.AutoField(primary_key=True, serialize=False)),
                ('atributo_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appIberiaExplorer.atributoplan')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UsuarioPreferencia',
                'verbose_name_plural': 'UsuarioPreferencias',
                'managed': True,
            },
        ),
    ]
# Generated by Django 5.0.3 on 2024-03-30 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appIberiaExplorer', '0025_alter_usuario_confirmation_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='confirmation_token',
            field=models.CharField(default='UvVtDno9DDgitKGcjHK6ct3jQmBvLeajZgM4k2xDn5HhvpYS4g', max_length=50),
        ),
    ]

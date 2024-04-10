# Generated by Django 5.0.3 on 2024-03-30 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appIberiaExplorer', '0010_alter_usuario_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='nombre',
        ),
        migrations.AddField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
# Generated by Django 4.0 on 2021-12-12 18:09

import certificados.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificados', '0002_alter_plantilla_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificado',
            name='codigo_verificacion',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='plantilla',
            name='archivo',
            field=models.FileField(upload_to='plantillas', validators=[certificados.models.validate_svg]),
        ),
    ]

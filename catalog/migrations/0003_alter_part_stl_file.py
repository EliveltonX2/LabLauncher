# Generated by Django 5.2.3 on 2025-06-19 21:31

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='stl_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to='parts_stl/', verbose_name='Arquivo STL'),
        ),
    ]

# Generated by Django 3.1.3 on 2020-11-30 07:49

import disaster_broadcaster.filepaths.FilePath
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disaster_broadcaster', '0012_auto_20201127_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='logo',
            field=models.FileField(null=True, upload_to=disaster_broadcaster.filepaths.FilePath.FilePath.logo),
        ),
    ]

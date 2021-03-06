# Generated by Django 3.0.7 on 2020-07-20 23:25

import bootcamp.storagemanager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200705_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, storage=bootcamp.storagemanager.GoogleCloudStorage(), upload_to='profile_pics', verbose_name='Profile picture'),
        ),
    ]

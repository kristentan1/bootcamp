# Generated by Django 3.0.7 on 2020-06-27 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/', verbose_name='Resume'),
        ),
    ]

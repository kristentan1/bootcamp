# Generated by Django 3.0.6 on 2020-05-21 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0002_auto_20200520_2054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='research',
            old_name='description',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='research',
            name='link',
        ),
        migrations.RemoveField(
            model_name='research',
            name='title',
        ),
    ]

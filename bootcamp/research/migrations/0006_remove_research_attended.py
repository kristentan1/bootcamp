# Generated by Django 3.0.6 on 2020-05-31 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0005_research_attended'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='research',
            name='attended',
        ),
    ]
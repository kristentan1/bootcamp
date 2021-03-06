# Generated by Django 3.0.6 on 2020-05-31 17:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0002_auto_20200520_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='attended',
            field=models.ManyToManyField(blank=True, related_name='attended_news', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(max_length=1000),
        ),
    ]

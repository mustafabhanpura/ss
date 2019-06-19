# Generated by Django 2.0.1 on 2019-06-17 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_auto_20190617_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='author',
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.7 on 2024-01-31 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0015_remove_address_user_address_new_name_address_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
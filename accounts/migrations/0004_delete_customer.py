# Generated by Django 4.2.7 on 2024-01-23 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_profile_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]

# Generated by Django 4.2.7 on 2024-01-24 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_profile_phone_alter_user_profile_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='phone',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='state',
            field=models.CharField(default=True, max_length=15, null=True),
        ),
    ]
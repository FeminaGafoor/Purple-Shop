# Generated by Django 4.2.7 on 2024-02-03 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_alter_user_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='phone',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
    ]

# Generated by Django 4.2.7 on 2024-01-28 16:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expiration_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 4.2.7 on 2024-02-16 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_paymentwallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='wallet',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-17 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.FloatField(default=True),
        ),
    ]
# Generated by Django 4.2.7 on 2024-02-02 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0021_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_note',
        ),
    ]

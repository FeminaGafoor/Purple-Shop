# Generated by Django 4.2.7 on 2024-02-08 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_rename_address_1_order_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[(1, 'New'), (2, 'Accepted'), (3, 'Preparing'), (4, 'On Shipping'), (5, 'Completed'), (6, 'Cancelled'), (7, 'Return')], default=1, null=True),
        ),
    ]

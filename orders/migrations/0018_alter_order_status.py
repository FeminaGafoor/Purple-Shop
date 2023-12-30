# Generated by Django 4.2.7 on 2023-12-30 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(1, 'New'), (2, 'Accepted'), (3, 'Preparing'), (4, 'On Shipping'), (5, 'Completed'), (6, 'Cancelled'), (7, 'Return')], default='New', max_length=10),
        ),
    ]

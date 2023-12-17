# Generated by Django 4.2.7 on 2023-12-17 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_address_line_1_user_profile_address_1_and_more'),
        ('orders', '0003_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user_profile'),
        ),
    ]

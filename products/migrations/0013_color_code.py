# Generated by Django 4.2.7 on 2023-12-19 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_size_remove_color_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
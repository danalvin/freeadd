# Generated by Django 3.2.6 on 2021-09-26 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_boosteditem_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
    ]
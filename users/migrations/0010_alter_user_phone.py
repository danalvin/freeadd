# Generated by Django 3.2.6 on 2021-10-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.PositiveIntegerField(blank=True, unique=True),
        ),
    ]

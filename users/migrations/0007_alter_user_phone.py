# Generated by Django 3.2.6 on 2021-09-26 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.PositiveIntegerField(default='701', unique=True),
            preserve_default=False,
        ),
    ]

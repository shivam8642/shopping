# Generated by Django 4.0.2 on 2022-03-08 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='email',
        ),
    ]
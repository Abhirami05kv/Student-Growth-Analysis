# Generated by Django 4.0.6 on 2022-07-09 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_parent_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='fee',
        ),
    ]

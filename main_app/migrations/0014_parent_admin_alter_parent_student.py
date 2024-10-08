# Generated by Django 4.2.6 on 2024-05-24 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0013_remove_parent_admin"),
    ]

    operations = [
        migrations.AddField(
            model_name="parent",
            name="admin",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="parent",
            name="student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main_app.student",
            ),
        ),
    ]

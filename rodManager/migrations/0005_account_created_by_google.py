# Generated by Django 4.2.6 on 2023-10-27 06:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rodManager", "0004_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="created_by_google",
            field=models.BooleanField(default=False),
        ),
    ]

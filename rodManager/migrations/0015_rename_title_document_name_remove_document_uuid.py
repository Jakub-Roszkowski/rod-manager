# Generated by Django 4.2.6 on 2023-11-29 14:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rodManager", "0014_payment_alter_garden_id_document"),
    ]

    operations = [
        migrations.RenameField(
            model_name="managerdocument",
            old_name="title",
            new_name="name",
        ),
        migrations.RemoveField(
            model_name="managerdocument",
            name="uuid",
        ),
    ]

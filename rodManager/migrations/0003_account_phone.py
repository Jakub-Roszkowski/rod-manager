# Generated by Django 4.2.6 on 2023-10-24 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodManager', '0002_remove_account_name_remove_account_permission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-23 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodManager', '0010_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Garden',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('sector', models.CharField(blank=True, max_length=255, null=True)),
                ('avenue', models.CharField(blank=True, max_length=255, null=True)),
                ('number', models.IntegerField()),
                ('area', models.FloatField(blank=True, null=True)),
                ('leaseholderID', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('dostępna', 'Available'), ('niedostępna', 'Unavailable')], default='dostępna', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GardenOffers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('predicted_rent', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('garden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rodManager.garden')),
                ('images', models.ManyToManyField(blank=True, to='rodManager.image')),
            ],
        ),
    ]

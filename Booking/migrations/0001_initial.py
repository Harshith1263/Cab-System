# Generated by Django 5.0.3 on 2024-03-27 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cab',
            fields=[
                ('cab_id', models.IntegerField(primary_key=True, serialize=False)),
                ('cab_name', models.CharField(max_length=100)),
                ('cab_type', models.CharField(max_length=100)),
                ('cab_status', models.CharField(max_length=100)),
                ('cab_driver_contact', models.CharField(max_length=100)),
                ('price_per_minute', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.IntegerField(primary_key=True, serialize=False)),
                ('location_name', models.CharField(max_length=100)),
                ('location_address', models.CharField(max_length=100)),
                ('location_pincode', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_datetime', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Booking.cab')),
            ],
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('distance_id', models.IntegerField(primary_key=True, serialize=False)),
                ('distance_distance', models.IntegerField()),
                ('distance_destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='Booking.location')),
                ('distance_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='Booking.location')),
            ],
        ),
    ]

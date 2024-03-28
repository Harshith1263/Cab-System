# Generated by Django 5.0.3 on 2024-03-27 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booking', '0003_alter_booking_booking_datetime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('connection_id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.IntegerField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='Booking.location')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='Booking.location')),
            ],
        ),
    ]
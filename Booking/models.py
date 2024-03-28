from django.db import models
from django.utils import timezone

# Create your models here.

class Cab(models.Model):
    cab_id = models.IntegerField(primary_key=True)
    cab_name = models.CharField(max_length=100)
    cab_type = models.CharField(max_length=100)
    cab_status = models.BooleanField()
    cab_driver_contact = models.CharField(max_length=100)
    price_per_minute = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.cab_name

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    booking_datetime = models.DateTimeField(auto_now_add=False)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE)
    email = models.EmailField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Booking #{self.booking_id}: {self.source} to {self.destination}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def book(self, source, destination, cab, email, cost):
        self.source = source
        self.destination = destination
        self.cab = cab
        self.email = email
        self.cost = cost
        self.save()

      
class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    location_name = models.CharField(max_length=100)
    location_address = models.CharField(max_length=100)
    location_pincode = models.IntegerField()

    def __str__(self):
        return self.location_name
    
    
class Connection(models.Model):
    connection_id = models.AutoField(primary_key=True)
    source = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='destination')
    time = models.IntegerField()

    def __str__(self):
        return f'{self.source} to {self.destination} in {self.time} minutes'
from django.contrib import admin
from .models import Cab, Booking, Location, Connection

# Register your models here.
admin.site.register({Cab, Booking, Location, Connection})
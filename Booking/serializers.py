from rest_framework import serializers
from .models import Cab, Booking


class CabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cab
        fields = '__all__'
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
class EstimatedTimeSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=100)
    destination = serializers.CharField(max_length=100)
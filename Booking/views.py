from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils import timezone
from .models import Cab, Booking, Location, Connection
from .serializers import CabSerializer, BookingSerializer, EstimatedTimeSerializer
from datetime import datetime, timedelta
from heapq import heappush, heappop
from decimal import Decimal

from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings


@api_view(['POST'])
def book_cab(request):
    source = request.data.get('source')
    destination = request.data.get('destination')
    email = request.data.get('email')
    booking_time_str = request.data.get('booking_time')
    required_cab = request.data.get('required_cab')
    booking_time_str=booking_time_str[:19]
    required_cab=int(required_cab)
    print("source",source)
    print("destination",destination)
    print("email",email)
    print("booking_time_str",booking_time_str)
    print("required_cab",required_cab)
    #check if data here is correct from console
    
    if Location.objects.filter(location_name=source).count() == 0 or Location.objects.filter(location_name=destination).count() == 0:
        return Response({'message': 'Invalid source or destination location.'}, status=400)

    booking_time = booking_time_str

    shortest_time, cabs = find_shortest_time_and_cab(source, destination, booking_time_str)
    
    if required_cab not in cabs:
        return Response({'message': 'The required cab is not available for the given route.'}, status=400)
    
    selected_cab = Cab.objects.get(cab_id=required_cab)
    
    print("shortest_time",shortest_time)
    print("selected_cab",selected_cab)
    
    if selected_cab:
        # Ensure shortest_time is a single value
        if isinstance(shortest_time, list):
            shortest_time = shortest_time[0]

        # Ensure selected_cab.price_per_minute is a Decimal object
        price_per_minute = Decimal(selected_cab.price_per_minute)

        # Calculate the cost
        cost = shortest_time * price_per_minute
        
        try:
            booking = Booking.objects.create(
                booking_datetime=booking_time,
                source=source,
                destination=destination,
                cab=selected_cab,
                email=email,
                cost=cost
            )
        except Exception as e:
            return Response({'message': f'Failed to create booking: {str(e)}'}, status=500)
          
        try:
            send_booking_email(booking)
        except Exception as e:
            booking.delete()
            return Response({'message': f'Failed to send booking confirmation email: {str(e)}'}, status=500)
        
        return Response({'message': f'Cab {selected_cab.cab_name} booked successfully!'}, status=201)
    else:
        return Response({'message': 'No available cabs for the given route.'}, status=400)





def find_shortest_time_and_cab(source, destination, booking_time_str):
    booking_time = timezone.make_aware(datetime.strptime(booking_time_str, "%Y-%m-%dT%H:%M:%S"))
    minimum_time = calculate_minimum_time(source, destination)
    available_cabs = []

    for cab in Cab.objects.all():
        if not cab.cab_status:
            continue

        is_available = True

        for booking in Booking.objects.filter(cab=cab):
            booking_start_time = booking.booking_datetime
            if booking_start_time is None:
                continue 

            booking_end_time = booking_start_time + timedelta(minutes=minimum_time)

            if (booking_start_time <= booking_time <= booking_end_time) or (booking_start_time <= booking_time + timedelta(minutes=minimum_time) <= booking_end_time):
                is_available = False
                break

        if is_available:
            available_cabs.append(cab.cab_id)
            
    print("minimum_time",minimum_time)
    print("available_cabs",available_cabs)

    return minimum_time, available_cabs

  
from heapq import heappop, heappush
from .models import Connection, Location

def calculate_minimum_time(source, destination):
    distances = {location: float('inf') for location in Location.objects.all()}
    source=Location.objects.get(location_name=source)
    destination=Location.objects.get(location_name=destination)
    distances[source] = 0
    pq = [(0, source)]
    while pq:
        current_distance, current_location = heappop(pq)
        if current_location == destination:
            return current_distance
        if current_distance > distances[current_location]:
            continue
        for connection in Connection.objects.filter(source=current_location):
            neighbor = connection.destination
            time_to_neighbor = current_distance + connection.time
            if time_to_neighbor < distances[neighbor]:
                distances[neighbor] = time_to_neighbor
                heappush(pq, (time_to_neighbor, neighbor))
    return None

# {
#     "source": "A",
#     "destination": "B",
#     "email": "example@example.com",
#     "booking_time": "2024-03-28T10:00:00",
#     "required_cab": 1
# }



def send_booking_email(booking):
    subject = 'Cab Booking Confirmation'
    message = f'Your cab from {booking.source} to {booking.destination} has been booked.\n' \
              f'Total cost: {booking.cost}\n' \
              f'Booking time: {booking.booking_datetime}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [booking.email])



@api_view(['GET'])
def CabDetail(request, cab_id):
    cab = Cab.objects.get(cab_id=cab_id)
    serializer = CabSerializer(cab)
    return Response(serializer.data)


@api_view(['GET'])
def CabList(request):
    cabs = Cab.objects.all()
    serializer = CabSerializer(cabs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def CalcEstimatedTime(request, source, destination):
    estimated_time = calculate_minimum_time(source, destination)
    if estimated_time is not None:
        return Response({'estimated_time': estimated_time}, status=200)
    else:
        return Response({'message': 'Failed to calculate estimated time'}, status=400)
    
@api_view(['GET'])
def CalcEstimatedCost(request, source, destination, cab_id):
    estimated_time = calculate_minimum_time(source, destination)
    cab = Cab.objects.get(cab_id=cab_id)
    price_per_minute = Decimal(cab.price_per_minute)
    cost = estimated_time * price_per_minute
    return Response({'estimated_cost': cost}, status=200)


from django.http import JsonResponse
from .models import Location, Cab, Booking
from decimal import Decimal


@api_view(['GET'])
def CheckCabAvailability(request, source, destination, booking_time, required_cab):
    # Ensure required_cab is an integer
    required_cab = int(required_cab)
    booking_time_str = booking_time[:19]

    if Location.objects.filter(location_name=source).count() == 0 or Location.objects.filter(location_name=destination).count() == 0:
        return JsonResponse({'message': 'Invalid source or destination location.'}, status=400)

    shortest_time, cabs = find_shortest_time_and_cab(source, destination, booking_time_str)
    
    if required_cab not in cabs:
        return JsonResponse({'message': 'The required cab is not available for the given route.'}, status=400)
    
    selected_cab = Cab.objects.get(cab_id=required_cab)
    
    if selected_cab:
        # Ensure shortest_time is a single value
        if isinstance(shortest_time, list):
            shortest_time = shortest_time[0]

        # Ensure selected_cab.price_per_minute is a Decimal object
        price_per_minute = Decimal(selected_cab.price_per_minute)

        # Calculate the cost
        cost = shortest_time * price_per_minute
        
        try:
            booking = Booking.objects.create(
                booking_datetime=booking_time_str,
                source=source,
                destination=destination,
                cab=selected_cab,
                cost=cost
            )
        except Exception as e:
            return JsonResponse({'message': f'Failed to create booking: {str(e)}'}, status=500)
          
        try:
            send_booking_email(booking)
        except Exception as e:
            booking.delete()
            return JsonResponse({'message': f'Failed to send booking confirmation email: {str(e)}'}, status=500)
        
        return JsonResponse({'message': f'Cab {selected_cab.cab_name} booked successfully!'}, status=201)
    else:
        return JsonResponse({'message': 'No available cabs for the given route.'}, status=400)

@api_view(['GET'])
def GetLocationList(request):
    locations = Location.objects.all()
    location_list = []
    for location in locations:
        location_list.append(location.location_name)
    return JsonResponse({'locations': location_list}, status=200)
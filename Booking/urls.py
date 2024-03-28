from django.urls import path
from . import views

urlpatterns = [
    path('bookcab/', views.book_cab, name='book-cab'),
    path('cab/<int:cab_id>/', views.CabDetail, name='cab-detail'),
    path('cablist/', views.CabList, name='cab-list'),
    path('calc-estimated-time/<str:source>/<str:destination>/', views.CalcEstimatedTime, name='CalcEstimatedTime'),
    path('estimate-cost/<str:source>/<str:destination>/<int:cab_id>/', views.CalcEstimatedCost, name='EstimateCost'),
    path('check-availability/<str:source>/<str:destination>/<str:booking_time>/<int:required_cab>', views.CheckCabAvailability, name='CheckCabAvailability'),
    path('get-locationnames/', views.GetLocationList, name='GetLocation'),
]
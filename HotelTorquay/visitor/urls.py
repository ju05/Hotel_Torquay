from django.urls import path
from .views import index, signup, signin, rooms_list, contact, bookings_list, booking_view

urlpatterns = [
    path('', index, name="index"),
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    path('rooms_list/', rooms_list, name="rooms_list"),
    path('bookings_list/', bookings_list, name="bookings_list"),
    path('contact/', contact, name="contact"),
    path('check_availability/', booking_view, name="check_availability"),
]

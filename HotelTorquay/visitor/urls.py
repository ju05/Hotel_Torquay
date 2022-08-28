from django.urls import path
from .views import booking_view, index, signup, signin, signout, contact, rooms_list, bookings_list, book_room

urlpatterns = [
    path('', index, name="index"),
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    path('signout/', signout, name="signout"),
    path('rooms_list/', rooms_list, name="rooms_list"),
    path('bookings_list/', bookings_list, name="bookings_list"),
    path('contact/', contact, name="contact"),
    path('check_availability/', booking_view, name="check_availability"),
    path('book_room/', book_room, name="book_room"),
]



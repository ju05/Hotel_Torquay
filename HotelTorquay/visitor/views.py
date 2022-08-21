from asyncio.format_helpers import _format_callback
from email.headerregistry import Group
from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, FormView
from django import forms
from .forms import AvailabilityForm, SignUpForm, ContactForm
from .models import Booking, Room
from visitor.booking_functions.availability import check_availability


def index(request):
    context = {'form':AvailabilityForm}
    return render(request, 'index.html', context)  

def signup(request):
    context = {'form':SignUpForm}
    if request.method =='POST':
        print('POST')
        form_filled = SignUpForm(request.POST)
        if form_filled.is_valid():
            form_filled.save()

            username = form_filled.cleaned_data['username']
            password = form_filled.cleaned_data['password']
            # Autenticate
            user = authenticate(username=username, password=password)
            regulars = Group.objects.get(name = 'Regurlars')
            regulars.user_set.add(user)

            login(request,user)
            return redirect('index')
        else:
            print(form_filled.errors)
            return render(request, 'signup.html', {'form': form_filled})
    return render(request, 'signup.html', context)

def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render (request, 'signin.html', {'form':AuthenticationForm(request.POST)})
    else:
        return render(request,'signin.html', {'form':AuthenticationForm(request.POST)})

def signout(request):
    if request.user.is_authenticate:
        logout(request)
    return redirect('signin')

def contact(request):
    if request.method == 'POST':
        form_filled = ContactForm(request.POST)
        if form_filled.is_valid():
            form_filled.save()
            messages.add_message(request, messages.SUCCESS, 'Your message was submited successfully, we will be in touch.')
            return HTTPResponse('Your message was sent. We`ll be in touch.')
    # else:
    #     return render(request, 'contact.html' {'form': ContactForm})

def rooms_list(request):
    context = {'rooms_list':Room.objects.all()}
    return render(request, 'rooms_list.html', context)

def bookings_list(request):
    context = {'bookings_list':Booking.objects.all()}
    return render(request, 'bookings_list.html', context)

def booking_view(request):
    context = {'form': AvailabilityForm}
    if request.method == 'POST':
        form_filled = AvailabilityForm(request.POST)
        if form_filled.is_valid():
            form_filled.save(commit=False)
            print(request.POST)

            # checking the availability for the room 
            rooms_list = Room.objects.filter(category = form_filled.cleaned_data['room_category'])
            available_rooms = []
            for room in rooms_list:
                if check_availability(room, form_filled.cleaned_data['check_in'], form_filled.cleaned_data['check_out']):
                    available_rooms.append(room)
                return render(request, 'rooms_list.html' ,{'rooms_list': available_rooms}) 
        else:
            print('not valid') 
    return render(request, 'check_availability.html', context)      

    #         # booking the room
    #         if len(available_rooms)>0:
    #             room = available_rooms[0]
    #             booking = Booking.objects.create(
    #                 user = request.user,
    #                 room = room,
    #                 check_in = form_filled.cleaned_data['check_in'],
    #                 check_out = form_filled.cleaned_data['check_out']
    #             )
    #             booking.save()
    #             return HTTPResponse('Your room was booked. Confirmation Number: 444')
    #         else: return HTTPResponse('All the rooms for this category are booked for those dates. Please choose anothe category or different dates')
    # return render(request, 'check_availability.html', context)
            

# class BookingView(FormView):
#     form_class = AvailabilityForm
#     template_name = 'check_availability.html'

    # def form_valid(self, form):
    #     data = form.cleaned_data
    #     rooms_list = Room.objects.filter(category = data['room_category'])
    #     available_rooms = []
    #     for room in rooms_list:
    #         if check_availability(room, data['check_in'], data['check_out']):
    #             available_rooms.append(room)
        
    #     if len(available_rooms) > 0:
    #         room = available_rooms[0]
    #         booking = Booking.objects.create(
    #             user = self.request.user,
    #             room = room,
    #             check_in = data['check_in'],
    #             check_out = data['check_out']
    #         )
    #         booking.save()
    #         return HTTPResponse(booking)
    #     else:
    #         return HTTPResponse('All the rooms for this category are booked, please choose a different room category')


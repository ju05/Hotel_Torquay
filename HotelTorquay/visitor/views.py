from email import message
from email.headerregistry import Group
from http.client import HTTPResponse
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, FormView
from django import forms
from .forms import AvailabilityForm, SignUpForm, ContactForm, BookingForm
from .models import Booking, Room
from visitor.booking_functions.availability import check_availability
from django.contrib.auth.decorators import login_required

def index(request):
    context = {'form':AvailabilityForm, 'contactform': ContactForm}
    return render(request, 'index.html', context)  

# -----------------------------------AUTHENTICATION--------------------------------------

def signup(request):
    context = {'form':SignUpForm, 'contactform': ContactForm}
    if request.method =='POST':
        print('POST')
        form_filled = SignUpForm(request.POST)
        if form_filled.is_valid():
            form_filled.save()

            username = form_filled.cleaned_data['username']
            password1 = form_filled.cleaned_data['password1']
            password2 = form_filled.cleaned_data['password2']
            # Autenticate
            user = authenticate(username=username, password1=password1, password2=password2)
            visitors = Group.objects.get(name = 'Visitors')
            visitors.user_set.add(user)
            messages.add_message(request, messages.INFO,'You are now logged in')
            login(request,user)            
            return redirect('index')
        else:
            print(form_filled.errors)
            return render(request, 'signup.html', context)
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
            messages.add_message(request, messages.ERROR, "your username or password are incorrect")
            return render (request, 'signin.html', {'form':AuthenticationForm(request.POST)})
    else:
        return render(request,'signin.html', {'form':AuthenticationForm , 'contactform': ContactForm})

def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')

# -------------------------------------------------END_AUTHENTICATION---------------------------------
# -------------------------------------------------CONTACT_FORM---------------------------------------
def contact(request):
    if request.method == 'POST':
        print('enter to post')
        form_filled = ContactForm(request.POST)
        if form_filled.is_valid():
            print('form valid')
            form_filled.save()
            messages.add_message(request, messages.SUCCESS, 'Your message was submited successfully, we will be in touch.')
            return render(request, 'check_availability.html', {'rooms_list':Room.objects.all(), 'contactform': ContactForm})
        else:
            return render(request, 'contact.html', {'contactform': ContactForm})
    return render(request, 'check_availability.html', {'rooms_list':Room.objects.all(),'contactform': ContactForm})


# --------------------------------------------------------------VISITORS---------------------------------------
def rooms_list(request):
    context = {'rooms_list':Room.objects.all(), 'contactform': ContactForm}
    return render(request, 'rooms_list.html', context)


@login_required(login_url='signin')
def book_room(user, room, check_in, check_out):
    Booking.objects.create(
        user_id = user.id,
        room_id = room.id,
        check_in = check_in,
        check_out = check_out)

    return redirect('book_confirmation')


def bookings_list(request):
    context = {'bookings_list':Booking.objects.all(), 'contactform': ContactForm}
    return render(request, 'bookings_list.html', context)

@login_required(login_url='signin')
def booking_view(request):
    context = {'form': AvailabilityForm, 'contactform': ContactForm}
    # the first POST when the Availability form is filled (after checking if there is a avalaible room in line 101)
    if request.method == 'POST':     
        # the second POST: if there is a available room, lets book it!
        if 'room' in request.POST:
            # the data is used to create a object of "Booking" model, wich is used for the BookingForm ModelForm
            filled_form = BookingForm(request.POST)
            if filled_form.is_valid():
                confirmation = filled_form.save()
                return render(request, 'book_confirmation.html', {'confirmation': confirmation, 'contactform': ContactForm})

        form_filled = AvailabilityForm(request.POST)
        if form_filled.is_valid():
            
            form_filled.save(commit = False)          
            # checking the availability for the room 
            rooms_list = Room.objects.filter(category = form_filled.cleaned_data['room_category'])
            available_rooms = []            
            for room in rooms_list:
                # calling the function imported from booking_functions to check availability for the specific room
                if check_availability(room, form_filled.cleaned_data['check_in'], form_filled.cleaned_data['check_out']):
                    available_rooms.append(room)  
            
        if len(available_rooms) > 0:
            confirmation_data = {}
            room = available_rooms[0]
            check_in = form_filled.cleaned_data['check_in']
            check_out = form_filled.cleaned_data['check_out']
            book_form = BookingForm(initial={'user': request.user, 'check_in': check_in, 'check_out': check_out, 'room': room})
            print('ROOM:', room)
            return render(request, 'book_room.html', {'book_form': book_form, 'room': room, 'contactform': ContactForm})          

        if len(available_rooms)==0:            
            messages.add_message(request, messages.INFO,'All the rooms for this category are booked. Please choose another one or available dates')
            return render(request, 'book_room.html', context)

    return render(request, 'check_availability.html' ,context)   


            


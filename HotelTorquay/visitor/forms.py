from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from functools import partial
from .models import Booking, Contact
from .widgets import DatePickerInput
from datetime import date

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

class AvailabilityForm(forms.ModelForm):
    room_categories=(
        ('STA','STANDARD'),
        ('COS','COSY'),
        ('FAM','FAMILY'),
        ('PRE','PREMIUM'),
        ('LUX','DELUXE'),
    )
    room_category = forms.ChoiceField(choices=room_categories, required=True)
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'room_category']
        widgets = {
            'check_in': forms.SelectDateWidget,
            'check_out': forms.SelectDateWidget,
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
       
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
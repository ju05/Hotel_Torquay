from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from functools import partial
from .models import Booking
from .widgets import DatePickerInput
from datetime import date


class AvailabilityForm(forms.Form):
    room_categories=(
        ('STA','STANDARD'),
        ('COS','COSY'),
        ('FAM','FAMILY'),
        ('PRE','PREMIUM'),
        ('LUX','DELUXE'),
    )
    room_category = forms.ChoiceField(choices=room_categories, required=True)
    persons = forms.IntegerField()
    check_in = forms.DateTimeField(required=True,
                                   input_formats=['%d/%m/%Y'],
                                   widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateTimeField(required=True,
                                    input_formats=['%d/%m/%Y'],
                                    widget=forms.DateInput(attrs={'type': 'date'}))

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    phone_number = forms.IntegerField()
    message = forms.Textarea()
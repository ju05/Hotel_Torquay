from tkinter import CASCADE
from django.db import models
from django.conf import settings

class Room(models.Model):
    
    room_categories=(
        ('STA','STANDARD'),
        ('COS','COSY'),
        ('FAM','FAMILY'),
        ('PRE','PREMIUM'),
        ('LUX','DELUXE'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=room_categories)
    beds = models.IntegerField()
    capacity = models.IntegerField()
    price = models.FloatField()
    def __str__(self):
        return f'{self.number} | {self.category} | beds: {self.beds} capacity: {self.capacity} persons | price: {self.price}'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f' {self.user} has booked {self.room} from {self.check_in} to {self.check_out}'

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.IntegerField()
    message = models.CharField(max_length=250)



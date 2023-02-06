from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class VehicleType(models.TextChoices):
    SUV = 'S', 'SUV'
    MINIBUS = 'M', 'MiniBus'
    BABYCAR = 'B', 'Baby Car'
    NORMALCAR = 'N', 'Normal Car'

class Vehicle(models.Model):
    id = models.AutoField(primary_key = True)
    driver = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=False, related_name='vehicle')

    vehicle_type = models.CharField(max_length=1, choices=VehicleType.choices, default=VehicleType.NORMALCAR)
    license_number = models.CharField(max_length = 50)
    max_capacity = models.PositiveIntegerField(default = 1)
    special_info = models.CharField(max_length = 100,null=False, blank = True)
    def __str__(self):
        return self.vehicle_type + "Driver: " + self.driver.username

    def get_absolute_url(self):
        return reverse('ridesharer:vehicle_info')

class RideStatus(models.TextChoices):
    OPEN = 'O', 'open'
    CONFIRMED = 'C', 'confirmed'
    FINISH = 'F', 'finish'

class Ride(models.Model):
    id = models.AutoField(primary_key = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,primary_key=False, related_name='ride')
    driver = models.ForeignKey(User, on_delete=models.CASCADE,primary_key=False, related_name='driver_ride',null=True)
    require_arrival_time = models.DateTimeField('arrival time',help_text='eg.2077-01-01 12:00')
    require_vehicle_type = models.CharField(max_length=1, choices=VehicleType.choices, default='', blank=True)
    create_time = models.DateTimeField('ride created date',null=True, blank=True)
    destination = models.CharField(max_length=200)
    passengers = models.PositiveIntegerField()
    allow_sharer = models.BooleanField(default=False)
    special_info = models.CharField('special requirement',max_length=200,blank=True)
    ride_status= models.CharField(max_length=1, choices=RideStatus.choices, default=RideStatus.OPEN)
    def get_absolute_url(self):
        return reverse('ridesharer:ride_list')
    def __str__(self):
        return "Owner: "+ self.owner.username+" Arrival time: " + str(self.require_arrival_time) + " dest: " + self.destination + " status: " + self.get_ride_status_display()

class ShareAction(models.Model):
    id = models.AutoField(primary_key = True)
    sharer = models.ForeignKey(User, on_delete=models.CASCADE,primary_key=False, related_name='share_actions')
    shared_ride = models.ForeignKey(Ride, on_delete=models.CASCADE,primary_key=False, related_name='sharing_actions')
    sharer_num = models.PositiveIntegerField(default = 1)
    def __str__(self):
        return "sharer: "+ self.sharer.username+" takes totally " + str(self.sharer_num) + " passengers to join the ride"
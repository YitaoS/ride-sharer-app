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

class Ride(models.Model):
    id = models.AutoField(primary_key = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.CharField(max_length=200)
    require_arrival_time = models.DateTimeField('arrival time',help_text='Format: 2022-01-01 12:00')
    require_vehicle_type = models.CharField(max_length=1, choices=VehicleType.choices, default=VehicleType.NORMALCAR, blank=True)
    create_time = models.DateTimeField('ride created date')
    destination = models.CharField(max_length=200)
    total_passengers = models.PositiveIntegerField()
    allow_sharer = models.BooleanField(default=False)
    special_info = models.CharField('special requirement',max_length=200,blank=True)
    class RideStatus(models.TextChoices):
        OPEN = 'O', 'open'
        CONFIRMED = 'C', 'confirmed'
        FINISH = 'F', 'finish'

    ride_status= models.CharField(max_length=1, choices=RideStatus.choices, default=RideStatus.OPEN)
    def get_absolute_url(self):
        return reverse('ridesharer:vehicle_info')
    def __str__(self):
        return "owner: " + self.owner.username + " dest: " + self.destination + " total: " + total_passengers
